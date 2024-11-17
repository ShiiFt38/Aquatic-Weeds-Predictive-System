import pandas as pd
import os
from models.db_export_utility import ExportUtility


class ExportReports:
    def __init__(self, db):
        self.db = db
        self.pdf_generator = ExportUtility(self.db)

    def save_to_excel(self, data_dict, output_path):
        """
        Save all DataFrames to a single Excel file with multiple sheets.

        Parameters:
        data_dict (dict): Dictionary of DataFrames
        output_path (str): Path where the Excel file should be saved
        """
        if not output_path:
            print("Invalid output path.")
            return

        print("Using Excel Writer...")
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in data_dict.items():
                    if not isinstance(df, pd.DataFrame):
                        print(f"Invalid data format for sheet {sheet_name}")
                        return
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                print("Excel report saved successfully.")
        except Exception as e:
            print(f"Error while writing to Excel: {e}")

    def save_to_csv(self, data_dict, base_file_path):
        """
        Save all DataFrames to separate CSV files.

        Parameters:
        data_dict (dict): Dictionary of DataFrames
        base_file_path (str): Base path for the CSV files (without extension)
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(base_file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Save each DataFrame to a separate CSV file
            saved_files = []
            for table_name, df in data_dict.items():
                # Create file path for each table
                file_name = f"{base_file_path}_{table_name}.csv"
                df.to_csv(file_name, index=False)
                saved_files.append(file_name)
                print(f"Saved {table_name} to {file_name}")

            return saved_files
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            raise

    def save_to_pdf(self, data_dict, file_path, logo_path, start_date, end_date):
        """
        Save data to a formatted PDF report.

        Parameters:
        data_dict (dict): Dictionary of DataFrames
        file_path (str): Path where the PDF file should be saved
        logo_path (str): Path to the logo image
        start_date (str): Start date of the report period
        end_date (str): End date of the report period
        """
        try:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'

            self.pdf_generator.create_pdf_report(
                data_dict,
                file_path,
                logo_path,
                start_date,
                end_date
            )
            print(f"Data successfully exported to PDF: {file_path}")
        except Exception as e:
            print(f"Error saving to PDF: {str(e)}")
            raise