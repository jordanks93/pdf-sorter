import os
import shutil
import pdfplumber

# Define categories and keywords
CATEGORIES = {
    "Credit Application": ["credit application"],
    "Invoices": ["invoice number", "invoice date", "invoice amount", "invoice due date"],
    "Deal Summary": ["deal summary", "transaction details"],
    "Credit Report": ["experian", "equifax", "credit report", "transunion", "credit bureau", "credit score", "fico"],
    "PayNet Report": ["paynet"],
    "Financials": ["balance sheet", "profit and loss", "financial statement", "income statement", "cash flow", "statement of cash flows", "statement of financial position", "statement of operations"],
    "Tax Returns": ["1040", "1120", "irs", "tax return", "w2", "1099", "tax form", "tax document", "tax filing"],
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

def sort_pdfs(input_dir):
    """Sort PDFs into a 'sorted' folder within the current folder by copying them in the correct order."""
    sorted_dir = os.path.join(input_dir, "sorted")
    os.makedirs(sorted_dir, exist_ok=True)

    sorted_files = {category: [] for category in CATEGORIES.keys()}
    sorted_files["Uncategorized"] = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            category = classify_pdf(file_path)
            sorted_files[category].append(filename)

    ordered_categories = [
        "Credit Application", "Invoices", "Deal Summary", "Credit Report",
        "PayNet Report", "Financials", "Tax Returns", "Uncategorized"
    ]

    for index, category in enumerate(ordered_categories):
        files = sorted_files[category]
        for filename in files:
            new_filename = f"{index + 1:02d}_{filename}"
            shutil.copy(
                os.path.join(input_dir, filename),
                os.path.join(sorted_dir, new_filename)
            )
            print(f"Copied {filename} to {sorted_dir} as {new_filename}")
            print(filename + " -> " + category)

if __name__ == "__main__":
    input_dir = get_directory("Enter the path to the folder containing PDFs: ")
    sort_pdfs(input_dir)
    print("Sorting complete!")
