# TODO: Amend the PDF export functionality
from sqlalchemy import create_engine
import pandas as pd
import os
from reportlab.lib import colors
import matplotlib.pyplot as plt
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from models.custom_pdf import CustomPDF

class ExportUtility():
    def __init__(self, db):
        self.db = db
        self.engine = create_engine('sqlite:///vegetation.db')
        self.styles = getSampleStyleSheet()
        # Create custom style for title
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        # Create custom style for section headers
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2E5090')  # Dark blue color
        )
        # Create custom style for dates
        self.date_style = ParagraphStyle(
            'DateRange',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=1,  # Center alignment
            spaceAfter=20
        )

    def generate_visualization(self, df, output_path):
        # Example: Create a bar chart of vegetation types
        if 'vegetation_type' not in df.columns:
            print("The 'vegetation_type' column is missing in the DataFrame.")
            return
        summary = df['vegetation_type'].value_counts()
        summary.plot(kind='bar', color='green')
        plt.title('Vegetation Type Distribution')
        plt.xlabel('Type')
        plt.ylabel('Count')
        plt.savefig(output_path)
        plt.close()

    def create_pdf_report(self, data_dict, file_path, logo_path, start_date, end_date):
        pdf = CustomPDF()
        pdf.logo_path = logo_path  # Assign logo path for the header
        pdf.add_page()

        # Add introduction
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(0, 10, f"This report covers the period from {start_date} to {end_date}.")
        pdf.ln(10)

        # Loop through DataFrames
        for table_name, df in data_dict.items():
            # Add section title
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, table_name.replace('_', ' ').title(), ln=True)
            pdf.ln(5)

            # Generate a summary chart and add it to the PDF
            chart_path = f"{table_name}_chart.png"
            self.generate_visualization(df, chart_path)
            if os.path.exists(chart_path):
                pdf.image(chart_path, x=10, y=pdf.get_y(), w=170)
                pdf.ln(70)  # Adjust spacing as needed
                os.remove(chart_path)

            # Add summarized data or insights (if applicable)
            if not df.empty:
                pdf.set_font('Arial', size=10)
                summary = df.describe(include='all').transpose()
                summary_text = summary.to_string()
                pdf.multi_cell(0, 10, f"Summary:\n{summary_text}")
            pdf.ln(10)

        # Output the PDF
        pdf.output(file_path)

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