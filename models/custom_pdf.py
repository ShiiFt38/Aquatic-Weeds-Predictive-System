from fpdf import FPDF
import os


class CustomPDF(FPDF):
    def header(self):
        # Add a logo (if available) and a title
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)  # Adjust dimensions as needed
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Vegetation Report', border=0, ln=1, align='C')
        self.ln(10)

    def footer(self):
        # Add a footer with the page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')