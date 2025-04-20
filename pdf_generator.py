"""
PDF Generator Module for TaxBot India
Generates detailed tax reports as downloadable PDFs
"""

from fpdf import FPDF
import datetime

class TaxReportPDF(FPDF):
    """Custom PDF class for generating tax reports"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Define the header of each page"""
        # Set font
        self.set_font("Arial", "B", 15)
        # Title
        self.cell(0, 10, "TaxBot India - Tax Report", 0, 1, "C")
        # Date
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, f"Generated on: {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}", 0, 1, "C")
        # Line break
        self.ln(5)
    
    def footer(self):
        """Define the footer of each page"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    
    def chapter_title(self, title):
        """Add a chapter title"""
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, "L", True)
        self.ln(4)
    
    def chapter_body(self, body):
        """Add chapter content"""
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 5, body)
        self.ln()
    
    def add_table_header(self, headers):
        """Add table header row"""
        self.set_font("Arial", "B", 11)
        self.set_fill_color(232, 232, 232)
        for header in headers:
            self.cell(40, 7, header, 1, 0, "C", True)
        self.ln()
    
    def add_table_row(self, data):
        """Add table data row"""
        self.set_font("Arial", "", 10)
        for item in data:
            self.cell(40, 6, str(item), 1, 0, "C")
        self.ln()

def generate_tax_report(user_data, old_regime, new_regime, better_regime, tips, ai_prediction=None):
    """
    Generate PDF tax report
    
    Args:
        user_data: Dictionary with user input data
        old_regime: Tax calculation for old regime
        new_regime: Tax calculation for new regime
        better_regime: Information about the better regime
        tips: List of tax saving tips
        ai_prediction: Optional AI prediction data
        
    Returns:
        PDF file bytes
    """
    pdf = TaxReportPDF()
    
    # Add first page
    pdf.add_page()
    
    # User Details
    pdf.chapter_title("Your Income Details")
    income_details = (
        f"Annual Income: Rs. {user_data['income']:,}\n"
        f"Section 80C Investments: Rs. {user_data['investments']:,}\n"
        f"Health Insurance Premium: Rs. {user_data['health_insurance']:,}\n"
        f"Home Loan Interest: Rs. {user_data['home_loan']:,}\n"
        f"Education Loan Interest: Rs. {user_data['edu_loan']:,}\n"
        f"HRA Exemption: Rs. {user_data['hra']:,}\n"
        f"Total Deductions: Rs. {user_data['total_deductions']:,}"
    )
    pdf.chapter_body(income_details)
    
    # Tax Calculation Section
    pdf.chapter_title("Tax Calculation")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, f"Old Regime Taxable Income: Rs. {user_data['old_regime_taxable']:,}", 0, 1)
    pdf.cell(0, 6, f"New Regime Taxable Income: Rs. {user_data['new_regime_taxable']:,}", 0, 1)
    pdf.ln(5)
    
    # Tax Comparison Table
    pdf.chapter_title("Tax Regime Comparison")
    pdf.add_table_header(["Details", "Old Regime", "New Regime"])
    
    # Format currency values - use "Rs." instead of ₹ symbol for encoding compatibility
    old_base_tax = f"Rs. {old_regime['base_tax']:,.2f}"
    old_cess = f"Rs. {old_regime['cess']:,.2f}"
    old_total = f"Rs. {old_regime['total_tax']:,.2f}"
    
    new_base_tax = f"Rs. {new_regime['base_tax']:,.2f}"
    new_cess = f"Rs. {new_regime['cess']:,.2f}"
    new_total = f"Rs. {new_regime['total_tax']:,.2f}"
    
    # Add table rows
    pdf.add_table_row(["Base Tax", old_base_tax, new_base_tax])
    pdf.add_table_row(["Cess (4%)", old_cess, new_cess])
    pdf.add_table_row(["Total Tax", old_total, new_total])
    
    # Better Regime Section
    pdf.ln(5)
    pdf.chapter_title("Recommended Tax Regime")
    better_regime_text = (
        f"Based on your inputs, the {better_regime['regime']} is better for you.\n"
        f"You will save approximately Rs. {better_regime['savings']:,.2f} by choosing this regime."
    )
    pdf.chapter_body(better_regime_text)
    
    # Detailed Tax Breakdown
    pdf.add_page()
    pdf.chapter_title("Detailed Tax Breakdown")
    
    # Add a description about tax slabs for reference
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Tax Slab Reference:", 0, 1)
    pdf.set_font("Arial", "", 10)
    
    # Old Regime Slabs
    pdf.multi_cell(0, 5, "Old Regime Tax Slabs (FY 2023-24):")
    old_slabs = (
        "- Income up to Rs. 2,50,000: No tax\n"
        "- Rs. 2,50,001 to Rs. 5,00,000: 5% of income exceeding Rs. 2,50,000\n"
        "- Rs. 5,00,001 to Rs. 10,00,000: Rs. 12,500 + 20% of income exceeding Rs. 5,00,000\n"
        "- Above Rs. 10,00,000: Rs. 1,12,500 + 30% of income exceeding Rs. 10,00,000\n"
        "- Plus: 4% Education & Health Cess on total tax amount"
    )
    pdf.multi_cell(0, 5, old_slabs)
    pdf.ln(3)
    
    # New Regime Slabs
    pdf.multi_cell(0, 5, "New Regime Tax Slabs (FY 2023-24):")
    new_slabs = (
        "- Income up to Rs. 3,00,000: No tax\n"
        "- Rs. 3,00,001 to Rs. 6,00,000: 5% of income exceeding Rs. 3,00,000\n"
        "- Rs. 6,00,001 to Rs. 9,00,000: Rs. 15,000 + 10% of income exceeding Rs. 6,00,000\n"
        "- Rs. 9,00,001 to Rs. 12,00,000: Rs. 45,000 + 15% of income exceeding Rs. 9,00,000\n"
        "- Rs. 12,00,001 to Rs. 15,00,000: Rs. 90,000 + 20% of income exceeding Rs. 12,00,000\n"
        "- Above Rs. 15,00,000: Rs. 1,50,000 + 30% of income exceeding Rs. 15,00,000\n"
        "- Plus: 4% Education & Health Cess on total tax amount"
    )
    pdf.multi_cell(0, 5, new_slabs)
    pdf.ln(5)
    
    # Add a subsection for comprehensive tax analysis
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Old Regime Tax Calculation:", 0, 1)
    pdf.set_font("Arial", "", 10)
    
    # Create detailed old regime tax breakdown
    old_regime_breakdown = (
        f"Base Income: Rs. {user_data['income']:,}\n"
        f"Total Deductions: Rs. {user_data['total_deductions']:,}\n"
        f"Taxable Income: Rs. {user_data['old_regime_taxable']:,}\n"
        f"Base Tax: Rs. {old_regime['base_tax']:,.2f}\n"
        f"Education & Health Cess (4%): Rs. {old_regime['cess']:,.2f}\n"
        f"Total Tax Liability: Rs. {old_regime['total_tax']:,.2f}\n"
    )
    pdf.multi_cell(0, 5, old_regime_breakdown)
    pdf.ln(3)
    
    # New regime breakdown
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "New Regime Tax Calculation:", 0, 1)
    pdf.set_font("Arial", "", 10)
    
    new_regime_breakdown = (
        f"Base Income: Rs. {user_data['income']:,}\n"
        f"Deductions: Not applicable in new regime\n"
        f"Taxable Income: Rs. {user_data['new_regime_taxable']:,}\n"
        f"Base Tax: Rs. {new_regime['base_tax']:,.2f}\n"
        f"Education & Health Cess (4%): Rs. {new_regime['cess']:,.2f}\n"
        f"Total Tax Liability: Rs. {new_regime['total_tax']:,.2f}\n"
    )
    pdf.multi_cell(0, 5, new_regime_breakdown)
    pdf.ln(3)
    
    # AI Prediction Section (if available)
    if ai_prediction:
        pdf.add_page()
        pdf.chapter_title("AI Tax Advisor Analysis")
        
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"AI Prediction: {ai_prediction['regime']}", 0, 1)
        pdf.set_font("Arial", "", 10)
        
        ai_text = (
            f"Our machine learning model has analyzed your financial profile and predicts that the {ai_prediction['regime']} "
            f"would be more beneficial for you with {ai_prediction['confidence']:.1f}% confidence.\n\n"
            f"Model Analysis: {ai_prediction['explanation']}\n\n"
            "Note: This AI prediction is based on patterns found in thousands of taxpayer profiles and "
            "serves as additional guidance alongside the traditional tax calculation."
        )
        pdf.multi_cell(0, 5, ai_text)
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, "How AI Predictions Work:", 0, 1)
        pdf.set_font("Arial", "", 10)
        
        ai_explanation = (
            "The TaxBot AI system uses advanced machine learning algorithms trained on historical tax data. "
            "It considers multiple factors in your financial profile, including:\n\n"
            "- Your income level relative to tax brackets\n"
            "- Ratio of deductions to total income\n"
            "- Types and amounts of specific deductions claimed\n"
            "- Age-related patterns in tax benefits\n\n"
            "This provides a complementary perspective to the traditional tax calculations."
        )
        pdf.multi_cell(0, 5, ai_explanation)
    
    # Tax Saving Tips
    pdf.add_page()
    pdf.chapter_title("Tax Saving Recommendations")
    
    for i, tip in enumerate(tips, 1):
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{i}. {tip}", 0, 1)
    
    # Disclaimer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    disclaimer = (
        "Disclaimer: This report is for informational purposes only and should not be considered as tax advice. "
        "Tax laws are subject to change. Please consult with a qualified tax professional for specific advice "
        "related to your tax situation."
    )
    pdf.multi_cell(0, 5, disclaimer)
    
    # Get the PDF content as bytes
    pdf_bytes = pdf.output(dest="S")
    # Return the bytes directly as they're already encoded
    return pdf_bytes
