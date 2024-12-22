import pdfplumber
import json

def pdf_to_json(pdf_path, json_path):
    """
    Converts a PDF file into a JSON format with text and tables.

    Args:
        pdf_path (str): Path to the input PDF file.
        json_path (str): Path to save the output JSON file.
    """
    extracted_data = {"pages": []}

    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()

            # Extract tables
            tables = page.extract_tables()

            # Prepare page data
            page_data = {
                "page_number": page_num + 1,
                "content": text,
                "tables": tables
            }

            # Append to extracted data
            extracted_data["pages"].append(page_data)

    # Save to JSON file
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"PDF data successfully saved to {json_path}")

# Example usage
if __name__ == "__main__":
    # Replace 'example.pdf' with your PDF file path
    pdf_to_json("/home/benjamin/Desktop/work/Tanami/Tanami/pdf/example.pdf", "output.json")

