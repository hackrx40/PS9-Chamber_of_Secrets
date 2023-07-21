import PyPDF2

def extract_pdf_metadata(file_path):
    metadata = {}
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        doc_info = pdf_reader.metadata
        metadata["Title"] = doc_info.get("/Title", None)
        metadata["Author"] = doc_info.get("/Author", None)
        metadata["Subject"] = doc_info.get("/Subject", None)
        metadata["CreationDate"] = doc_info.get("/CreationDate", None)
        metadata["ModDate"] = doc_info.get("/ModDate", None)
        
        # Extract Producer and Creator information
        metadata["Producer"] = doc_info.get("/Producer", None)
        metadata["Creator"] = doc_info.get("/Creator", None)

    return metadata

def is_metadata_suspicious(metadata):
    # Check for inconsistent or unusual timestamps
    creation_date = metadata.get("CreationDate", None)
    mod_date = metadata.get("ModDate", None)
    if creation_date and mod_date:
        if creation_date > mod_date:
            return True

    # Examine the source information for unusual patterns
    author = metadata.get("Author", None)
    subject = metadata.get("Subject", None)
    if author and subject:
        if author.lower() not in subject.lower() and subject.lower() not in author.lower():
            return True

    # Verify if essential metadata fields are missing or empty
    if not metadata.get("Title") or not metadata.get("Author"):
        return True

    # If none of the suspicious conditions are met, return False
    return False

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\Prathmesh\Downloads\Amazon 2 F sign.pdf"

    metadata = extract_pdf_metadata(pdf_file_path)

    print("PDF Metadata:")
    print("------------")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    if is_metadata_suspicious(metadata):
        print("Document is fraudulent due to suspicious metadata.")
    else:
        print("Metadata analysis passed. Proceed to the next stage.")