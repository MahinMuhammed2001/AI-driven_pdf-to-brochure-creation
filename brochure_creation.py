import fitz  # PyMuPDF - Library for reading and extracting content from PDF files
import os  # Library to interact with the operating system (e.g., create directories)
import spacy  # Library for Natural Language Processing (NLP)
from reportlab.lib.pagesizes import letter  # For setting the page size to letter
from reportlab.lib import colors  # For adding colors to the PDF content
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # For defining styles for text
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image  # For creating the PDF content
from spacy import displacy  # For visualizing parsed entities (not used in this case)
from collections import Counter  # For counting occurrences of words/entities (not used in this case)
import matplotlib.pyplot as plt  # For plotting graphs (not used in this case)
from collections import defaultdict  # A dictionary that returns a default value when a key doesn't exist

# Function to extract text from the PDF file
def extract_text_from_pdf(pdf_path):
    """Extracts text from all pages of the PDF using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)  # Open the PDF document
    text = ""  # Initialize an empty string to hold all the extracted text
    for page_num in range(len(doc)):  # Loop through each page of the PDF
        page = doc.load_page(page_num)  # Load the current page
        text += page.get_text("text")  # Extract the text from the page and add it to the 'text' string
    return text  # Return the extracted text

# Load the spaCy NLP model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")  # Use the small English model for NER

# Function to extract key information from the extracted text using NLP
def extract_nlp_data(extracted_text):
    """Extracts relevant data using NLP (Product Name, Key Features, etc.)."""
    doc = nlp(extracted_text)  # Process the extracted text with spaCy's NLP model
    extracted_data = defaultdict(list)  # Initialize a dictionary to hold the extracted data

    # Loop through the recognized entities in the text (e.g., product name, brand)
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":  # If the entity is a product name
            extracted_data["product_name"].append(ent.text)  # Add the product name to the data dictionary
        elif ent.label_ == "ORG":  # If the entity is a brand or organization
            extracted_data["brand"].append(ent.text)  # Add the brand to the data dictionary
        elif ent.label_ == "GPE":  # If the entity is a location (e.g., country)
            extracted_data["location"].append(ent.text)  # Add the location to the data dictionary
        elif ent.label_ == "MONEY":  # If the entity is a price
            extracted_data["price"].append(ent.text)  # Add the price to the data dictionary
        elif ent.label_ == "DATE":  # If the entity is a date
            extracted_data["date"].append(ent.text)  # Add the date to the data dictionary

    # Use a simple heuristic to extract sentences that mention "feature" or "spec"
    for sentence in doc.sents:
        if "feature" in sentence.text.lower() or "spec" in sentence.text.lower():
            extracted_data["key_features"].append(sentence.text)  # Add the sentence to the key_features list

    return extracted_data  # Return the extracted data

# Function to refine the extracted product overview from the text
def refine_overview(extracted_text):
    """Refines the extracted text to get the relevant product overview."""
    overview_start = "C42GM is an LTE"  # Define the start marker for the product overview
    overview_end = "Copyright © 2024 Cavli Inc."  # Define the end marker for the product overview

    # Find the start and end positions of the overview text in the extracted text
    start_idx = extracted_text.find(overview_start)
    end_idx = extracted_text.find(overview_end)
    
    if start_idx != -1 and end_idx != -1:  # If both start and end markers are found
        overview_text = extracted_text[start_idx:end_idx].strip()  # Extract the overview text
    else:
        overview_text = "Product overview could not be extracted correctly."  # If markers are not found, return a placeholder

    return overview_text  # Return the extracted overview text

# Function to extract images from the PDF
def extract_images_from_pdf(pdf_path, image_output_dir):
    """Extract images from a PDF file and save them to the specified directory."""
    if not os.path.exists(image_output_dir):  # If the output directory doesn't exist
        os.makedirs(image_output_dir)  # Create the directory

    doc = fitz.open(pdf_path)  # Open the PDF document
    image_list = []  # Initialize an empty list to hold the image file paths

    # Loop through each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load the current page
        img_list = page.get_images(full=True)  # Get the images from the page

        # Loop through each image on the page
        for img_index, img in enumerate(img_list):
            xref = img[0]  # Get the image reference number
            base_image = doc.extract_image(xref)  # Extract the image using the reference
            image_bytes = base_image["image"]  # Get the image data
            image_filename = os.path.join(image_output_dir, f"image_{page_num+1}_{img_index+1}.png")  # Create the image file path
            with open(image_filename, "wb") as img_file:  # Save the image to the specified directory
                img_file.write(image_bytes)
            image_list.append(image_filename)  # Add the image file path to the list

    return image_list  # Return the list of image file paths

# Function to create the final brochure PDF
def create_pdf(brochure_data, output_path, extracted_images):
    doc = SimpleDocTemplate(output_path, pagesize=letter)  # Create a SimpleDocTemplate for the PDF
    story = []  # Initialize an empty list to hold the content of the brochure

    # Define styles for the brochure
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    heading_style = ParagraphStyle('Heading', parent=styles['Normal'], fontSize=18, fontName='Helvetica-Bold', textColor=colors.darkblue, spaceAfter=12, alignment=0)  # Style for headings
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, fontName='Helvetica', textColor=colors.black, spaceAfter=6)  # Style for body text
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, fontName='Helvetica', textColor=colors.grey, spaceBefore=6)  # Style for footer text

    # Add the product title and description
    story.append(Paragraph("<font size=22><b>C42GM</b></font>", heading_style))  # Add product title
    story.append(Spacer(1, 12))  # Add space after the title
    story.append(Paragraph("<font size=14><i>Advanced LTE Cat M1/NB1/NB2 Module</i></font>", body_style))  # Add product description
    story.append(Spacer(1, 24))  # Add space after the description

    # Add product overview section
    story.append(Paragraph(brochure_data['overview']['title'], heading_style))  # Add title for the overview section
    story.append(Spacer(1, 12))
    story.append(Paragraph(brochure_data['overview']['content'], body_style))  # Add the overview content
    story.append(Spacer(1, 24))

    # Add product name and image if extracted
    if extracted_images:
        image_path_1 = extracted_images[0]  # Get the first image path
        story.append(Spacer(1, 0))  # Add no vertical space
        story.append(Paragraph('<b>Product Name:</b>', body_style))  # Add product name label
        story.append(Spacer(1, 12))
        story.append(Paragraph("C42GM", body_style))  # Add product name text
        story.append(Spacer(1, 12))
        story.append(Image(image_path_1, width=100, height=24))  # Add the image next to the product name
        story.append(Spacer(1, 12))

    # Add additional images if available
    if len(extracted_images) > 2:
        image_path_2 = extracted_images[2]  # Get the second image path
        story.append(Spacer(1, 24))
        story.append(Image(image_path_2, width=200, height=100))  # Add the second image under the overview

    # Add key features section
    story.append(Paragraph("<b>Key Features</b>", heading_style))  # Add section title for key features
    for highlight in brochure_data['key_highlights']:
        story.append(Paragraph(f"<font size=10>&#8226; {highlight}</font>", body_style))  # Add each key feature as a bullet point
        story.append(Spacer(1, 6))  # Add space after each feature
    story.append(Spacer(1, 36))  # Add space after key features

    # Add technical specifications section
    story.append(Paragraph("Technical Specifications", heading_style))  # Add section title for technical specifications
    for subheading, content in brochure_data['basic_module_info'].items():
        story.append(Paragraph(f"<b>{subheading}:</b> {content}", body_style))  # Add each specification
        story.append(Spacer(1, 6))  # Add space after each specification

    story.append(Spacer(1, 24))  # Add space after technical specifications

    # Add images if available
    if len(extracted_images) > 3:
        image_path_3 = extracted_images[3]  # Get the fourth image path
        story.append(Spacer(1, 24))
        story.append(Image(image_path_3, width=150, height=100))  # Add the image under the specifications section

    # Add footer
    story.append(Spacer(1, 24))  # Add space before footer
    story.append(Paragraph(brochure_data['footer'], footer_style))  # Add footer text

    doc.build(story)  # Build and generate the PDF from the story

# Function to structure the extracted data into the desired format
def structure_data(text):
    """Structure extracted text into the desired format for the PDF."""
    overview_text = refine_overview(text)  # Get the refined product overview
    
    return {
        "overview": {
            "title": "C42GM Product Overview",  # Set the title for the overview
            "content": overview_text  # Set the content for the overview
        },
        "key_highlights": [  # Key features of the product
            "Integrated Hubble eSIM",
            "Modem Intelligence Cloud",
            "Global GNSS Support",
            "Sigfox Certified NB-IoT Module",
            "Classic CAN Interface",
            "DRX & eDRX modes"
        ],
        "basic_module_info": {  # Technical specifications of the product
            "Application Processor Specification": "1.5GHz, ROM: 16 MB/32 MB",
            "Supported Brands": "LTE",
            "Communication Protocols": "HTTP(S), MQTT(S), Sigfox, CAN",
            "Temperature Range": "-30°C to +75°C",
            "Interfaces": "3xUART, 1xANT, 1xGNSS_ANT, 1xSDIO.",
            "Packaging": "Dimensions 26.5 x 22.5 x 2.3 mm, LGA Package",
            "Network Speed": "Up to 100 Mbps",
            "Constellation Coverage": "GPS/ BeiDou & QZSS",
            "Power Characteristics": "Voltage Range: 3.1V to 4.2V"
        },
        "footer": """  # Footer text to be displayed at the bottom of the brochure
            Copyright © 2024.V1.0 Cavli Inc., All Rights Reserved
            www.cavliwireless.com
            HQ address: Cavli Inc.,99 South Almaden Blvd., Suite 600, San Jose, California, 95113
            Email: solutions@cavliwireless.com
        """
    }

# Main function to execute the script
if __name__ == "__main__":
    # Set the paths for the PDF, image output directory, and final brochure output
    pdf_path = r"D:\AI-Driven Product Brochure Creation\C42GM_1725347073674.pdf"
    image_output_dir = "extracted_images"
    output_pdf_path = "C42GM_Brochure.pdf"
    
    # Extract images from the PDF
    extracted_images = extract_images_from_pdf(pdf_path, image_output_dir)
    
    # Extract the text from the PDF to populate the brochure content
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Structure the extracted text into the desired format for the brochure
    brochure_data = structure_data(extracted_text)
    
    # Generate the PDF brochure
    create_pdf(brochure_data, output_pdf_path, extracted_images)
    
    # Print the path of the generated brochure
    print(f"Brochure created at: {output_pdf_path}")
