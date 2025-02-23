import os
import shutil
import pdfplumber

# Define categories and keywords
CATEGORIES = {
    "Credit Application": ["credit application"],
    "Invoices": ["invoice number", "bill to"],
    "Deal Summary": ["deal summary", "transaction details"],
    "Credit Report": ["experian", "equifax", "credit report"],
    "PayNet Report": ["paynet"],
    "Financials": ["balance sheet", "profit and loss", "financial statement"],
    "Tax Returns": ["1040", "1120", "irs", "tax return", "W2"]
}

def get_directory(prompt):
    """Prompt the user to input a directory path."""
    while True:
        directory = input(prompt).strip()
        if os.path.exists(directory):
            return directory
        print("Invalid path. Please enter a valid directory.")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text.lower()

def classify_pdf(pdf_path):
    """Classify a PDF based on extracted text."""
    text = extract_text_from_pdf(pdf_path)
    for category, keywords in CATEGORIES.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Uncategorized"

def sort_pdfs(input_dir, output_dir):
    """Sort PDFs into categorized folders."""
    for category in CATEGORIES.keys():
        os.makedirs(os.path.join(output_dir, category), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "Uncategorized"), exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            category = classify_pdf(file_path)
            dest_dir = os.path.join(output_dir, category)
            shutil.move(file_path, os.path.join(dest_dir, filename))
            print(f"Moved {filename} to {category}/")

if __name__ == "__main__":
    input_dir = get_directory("Enter the path to the folder containing PDFs: ")
    output_dir = get_directory("Enter the path to the folder where sorted PDFs should be placed: ")
    sort_pdfs(input_dir, output_dir)
    print("Sorting complete!")
