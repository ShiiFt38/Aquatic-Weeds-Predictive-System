import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

class ExportUtility():
    def __init__(self, db):
        self.db = db
        self.engine = create_engine('sqlite:///vegetation.db')

    def export_vegetation_data(self, start_date, end_date):
        """
        Export data from all related tables within a date range.

        Parameters:
        db_path (str): Path to the SQLite database
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

        Returns:
        dict: Dictionary containing DataFrames for each table and a merged DataFrame
        """

        # Query for image_scans
        image_scans_query = """
            SELECT *
            FROM image_scans
            WHERE date BETWEEN ? AND ?
        """

        # Query for vegetation_features with joined image scan data
        vegetation_query = """
            SELECT 
                v.*,
                i.image_path,
                i.total_vegetation_count
            FROM vegetation_features v
            LEFT JOIN image_scans i ON v.date = i.date
            WHERE v.date BETWEEN ? AND ?
        """

        # Query for weather data with joined image scan data
        weather_query = """
            SELECT 
                w.*,
                i.image_path,
                i.total_vegetation_count
            FROM weather_data w
            LEFT JOIN image_scans i ON w.date = i.date
            WHERE w.date BETWEEN ? AND ?
        """

        # Execute queries and create DataFrames
        image_scans_df = pd.read_sql_query(
            image_scans_query,
            self.engine,
            params=(start_date, end_date)
        )

        vegetation_df = pd.read_sql_query(
            vegetation_query,
            self.engine,
            params=(start_date, end_date)
        )

        weather_df = pd.read_sql_query(
            weather_query,
            self.engine,
            params=(start_date, end_date)
        )

        # Create a merged DataFrame containing all related data
        merged_df = pd.merge(
            vegetation_df,
            weather_df[['date', 'max_temp', 'min_temp', 'precipitation',
                        'rainfall', 'max_wind']],
            on='date',
            how='left'
        )

        # Return all DataFrames in a dictionary
        return {
            'image_scans': image_scans_df,
            'vegetation_features': vegetation_df,
            'weather_data': weather_df,
            'merged_data': merged_df
        }