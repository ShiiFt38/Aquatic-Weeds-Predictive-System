from sqlalchemy import create_engine, text
import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

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

    def create_pdf_report(self, data_dict, file_path, logo_path, start_date, end_date):
        """
        Create a PDF report with logo and formatted data tables.

        Parameters:
        data_dict (dict): Dictionary of DataFrames
        file_path (str): Output PDF file path
        logo_path (str): Path to logo image
        start_date (str): Start date of the report period
        end_date (str): End date of the report period
        """
        doc = SimpleDocTemplate(
            file_path,
            pagesize=landscape(letter),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        # Store all elements that will go into the PDF
        elements = []

        # Add logo
        logo = Image(logo_path, width=2 * inch, height=2 * inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 20))

        # Add title
        elements.append(Paragraph("Aquatic Weeds Predictive System", self.title_style))

        # Add date range
        date_text = f"Report Period: {start_date} to {end_date}"
        elements.append(Paragraph(date_text, self.date_style))
        elements.append(Spacer(1, 20))

        # Process each DataFrame
        for table_name, df in data_dict.items():
            # Add section header
            section_title = table_name.replace('_', ' ').title()
            elements.append(Paragraph(section_title, self.section_style))

            # Convert DataFrame to list of lists for ReportLab
            data = [df.columns.tolist()] + df.values.tolist()

            # Create table
            table = Table(data, repeatRows=1)

            # Style the table
            table_style = TableStyle([
                # Header style
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
            ])
            table.setStyle(table_style)

            # Add table to elements
            elements.append(table)
            elements.append(Spacer(1, 30))

        # Build PDF
        doc.build(elements)

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