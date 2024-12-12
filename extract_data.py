import fitz  # PyMuPDF

# Function to extract text from PDF using PyMuPDF (fitz)
def extract_text_from_pdf(pdf_path):
    """Extracts text from all pages of the PDF using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")  
    return text

# Function to save the extracted text to a text file
def save_text_to_file(text, output_txt_path):
    """Save extracted text to a text file."""
    with open(output_txt_path, "w", encoding="utf-8") as output_file:
        output_file.write(text)

# Main execution
if __name__ == "__main__":
    pdf_path = r"D:\AI-Driven Product Brochure Creation\C42GM_1725347073674.pdf"  # Path to your PDF
    output_txt_path = r"D:\AI-Driven Product Brochure Creation\extracted_text.txt"  # Path to save the extracted text
    
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Save the extracted text to the file
    save_text_to_file(extracted_text, output_txt_path)
    
    print(f"Text extraction complete. The extracted text is saved to {output_txt_path}")
