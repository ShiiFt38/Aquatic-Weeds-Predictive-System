import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3


class ExportReports:
    def __init__(self, db):
        self.db = db

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