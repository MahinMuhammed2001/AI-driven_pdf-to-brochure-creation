# AI-Driven Product Brochure Creation  

 **Code & Methodology**  
   - Python code that uses **AI (NLP)** to extract data, structure it, and create a visually appealing brochure.  

## Project Structure

- **`brochure_creation.py`**: Main script that extracts data, processes the information, and generates the final brochure in PDF format.
- **`extract_data.py`**: Script used to extract all the text content from the PDF document.
- **`extracted_images/`**: Folder where all images extracted from the PDF are stored.
- **Output**: The generated brochure is saved as `C42GM_Brochure.pdf`.
---

## Features

- **Document Parsing**: Extracts text and images from a PDF using `PyMuPDF`.
- **AI-Based Data Extraction**: Uses `spaCy` for Named Entity Recognition (NER) to extract product name, features, specifications, and other relevant details.
- **Data Structuring**: Organizes the extracted data into sections like Product Overview, Key Features, and Technical Specifications.
- **PDF Generation**: Creates a visually appealing brochure using `ReportLab`, integrating extracted text, images, and custom styles.

## **How It Works**  

### **1. Document Parsing (AI-based Extraction)**  
The project uses the `PyMuPDF` library to extract text and images from the provided PDF document. AI techniques, specifically `spaCy`'s NLP model, are employed for the following tasks:  
- Identifying entities such as product names, key features, technical specifications, and other relevant details.  
- Extracting data accurately while handling missing or incomplete details.  

### **2. Data Structuring**  
The extracted data is organized into predefined sections:  
- **Product Overview**: A brief introduction to the product.  
- **Key Features**: Highlighted product features.  
- **Technical Specifications**: Detailed specifications such as processor type, communication protocols, and more.  


This structured data is used to ensure clarity in the final brochure.  



## **Challenges Faced**  
- **Usage Instructions Extraction**:  
  Usage instructions were not explicitly available in the document. A heuristic approach was applied to infer or summarize relevant content.  
- **Design and Layout**:  
  Ensuring the brochure’s layout was visually appealing and aligned with professional standards required careful planning.  

---

## **How AI Was Used**  
1. **spaCy NLP**:  
   - Named Entity Recognition (NER) to identify important elements like product names, brands, and key features.  
   - Text summarization to refine the overview and usage instructions.  

2. **AI in Content Generation**:  
   - Filling gaps where data was incomplete using descriptive patterns.  
   - Automatic formatting of extracted data into structured sections.  

---
## Output

- **Brochure File**: `C42GM_Brochure.pdf` is a professional 2-page brochure containing:
  - Product Overview
  - Key Features
  - Technical Specifications
  - Footer with contact details

## Code Explanation
For creating a professional 2-page PDF brochure by extracting key data from a technical specification document using AI techniques. The code leverages the PyMuPDF library to extract text and images from a PDF file, and the spaCy NLP model to identify and extract meaningful entities like product names, features, and specifications. The extracted data is then refined and structured into predefined sections such as Product Overview, Key Features, and Technical Specifications using the structure_data function. These sections ensure the data is well-organized and formatted for the final brochure.

The PDF creation process uses the ReportLab library to design and generate the brochure. Custom styles are applied for headings, body text, and a footer to ensure a professional layout. The brochure incorporates images extracted from the source document and arranges them appropriately within the design. AI enhances the content by summarizing or refining text where necessary. The result is a visually appealing and informative brochure that effectively communicates the product’s key information, including usage instructions and technical details.


### Problem Faced with Poppler

During the development of this project, I initially tried using **Poppler** to extract images and text from the PDF. However, I faced issues with the installation and configuration of Poppler on my PC. Despite downloading the Poppler tool and setting the correct system path, I kept encountering an error that stated the file was missing. I attempted to resolve this by checking system paths, reinstalling Poppler, and using different versions, but the issue persisted.

### Solution with Fitz

Given that Poppler was not working for me, I decided to use **Fitz** (also known as PyMuPDF), which is a Python library designed for extracting text, images, and metadata from PDF files. Fitz worked well for my use case, allowing me to successfully extract both text and images from the PDF files. Although **Poppler** is a more advanced and feature-rich tool, **Fitz** proved to be a suitable alternative in this case for my project.


