import os                                                                                                                                                                                                          
from fpdf import FPDF
from state.state_types import State

def export_to_pdf(state: State):
    company_name = state['company_name']
    filename = f"cover_letter_{company_name}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    text = state['final_cover_letter_content']
    
    paragraphs = text.split("\n\n")
    
    for para in paragraphs:
        pdf.multi_cell(0, 10, para.strip())
        pdf.ln()  # Add space between paragraphs
    
    pdf.output(filename)