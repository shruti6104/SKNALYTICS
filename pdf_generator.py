from fpdf import FPDF

def generate_pdf(data_list, product_name, filename="product_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Product Summary: {product_name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    for item in data_list:
        pdf.cell(200, 10, f"Platform: {item['Platform']}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 10, f"Product: {item['Product']}")
        pdf.cell(200, 8, f"Price: ₹{item['Price (₹)']}  |  Rating: {item['Rating']}", ln=True)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(200, 8, f"URL: {item['URL']}", ln=True, link=item['URL'])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)

    pdf.output(filename)
    return filename
