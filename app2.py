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
        metadata["PageCount"] = len(pdf_reader.pages)

        # Extract PageLayout and PageMode
        trailer = pdf_reader.trailer
        if "/PageLayout" in trailer:
            metadata["PageLayout"] = trailer["/PageLayout"]
        else:
            metadata["PageLayout"] = None

        if "/PageMode" in trailer:
            metadata["PageMode"] = trailer["/PageMode"]
        else:
            metadata["PageMode"] = None

    return metadata

def is_metadata_suspicious(metadata):
    # Check for inconsistent or unusual timestamps
    creation_date = metadata.get("CreationDate", None)
    mod_date = metadata.get("ModDate", None)
    if creation_date and mod_date:
        if creation_date > mod_date:
            return True

    # Examine the source information for unusual patterns
    producer = metadata.get("Producer", None)
    creator = metadata.get("Creator", None)
    pdf_editing_tool_names = [
    "adobe",
    "nitro",
    "foxit",
    "pdf-xchange",
    "infix",
    "phantompdf",
    "ilovepdf",
    "smallpdf",
    "sejda",
    "pdfescape",
    "pdfsam",
    "pdfpen",
    "pdf24",
    "masterpdf",
    "pdfexpert",
    "pdfcandy",
    "pdfmate",
    "pdfpro",
    "pdfill",
    "pdfshaper"
]
    for tool_name in pdf_editing_tool_names:
        if producer and tool_name.lower() in producer.lower():
            return True
        if creator and tool_name.lower() in creator.lower():
            return True

    # If none of the suspicious conditions are met, return False
    return False

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\Prathmesh\Downloads\Forgery document use case\Forgery document use case\Hackathon\Health doc\INVGR_31-08-2022 001311_179006254.pdf"

    metadata = extract_pdf_metadata(pdf_file_path)

    print("PDF Metadata:")
    print("------------")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    if is_metadata_suspicious(metadata):
        print("Document is fraudulent due to suspicious metadata.")
    else:
        print("Metadata analysis passed. Proceed to the next stage.")