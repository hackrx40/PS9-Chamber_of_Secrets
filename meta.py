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

    # Examine the source information for genuine software names
    producer = metadata.get("Producer", None)
    creator = metadata.get("Creator", None)
    
    # List of genuine software names commonly used for creating/editing PDFs
    genuine_software_names = [
        "Microsoft Word",
        "Microsoft Excel",
        "Microsoft PowerPoint",
        "Adobe Acrobat",
        "Adobe InDesign",
        "Adobe Illustrator",
        "LibreOffice",
        "Google Docs",
        "Foxit PhantomPDF",
        "Nitro Pro",
        "PDFelement",
        "WPS Office",
        "Pages (Apple)",
        "Numbers (Apple)",
        "Keynote (Apple)",
        "OpenOffice",
        "CorelDRAW",
        "Sketch (Bohemian Coding)",
        "Inkscape",
        "GIMP",
        "Affinity Publisher",
        "Affinity Designer",
        "Scribus",
        "QuarkXPress",
        "iText",
        # Add more genuine software names as needed
    ]

    # List of fraudulent editing tool names
    fraudulent_editing_tools = [
        "adobe",
    "Adobe PDF librar",
    "Adobe Illustrator",
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
    "adobe",
    "pdf",
    "acrobat",
    "foxit",
    "nitro",
    "editor",
    "creator",
    "converter",
    "writer",
    "reader",
    "tool",
    "edit",
    "create",
    "convert",
        # Add more fraudulent editing tool names as needed
    ]

    if producer and any(tool.lower() in producer.lower() for tool in fraudulent_editing_tools):
        return True

    if creator and any(tool.lower() in creator.lower() for tool in fraudulent_editing_tools):
        return True

    # If genuine software name is found, return False (not suspicious)
    if producer and any(genuine_name.lower() in producer.lower() for genuine_name in genuine_software_names):
        return False

    if creator and any(genuine_name.lower() in creator.lower() for genuine_name in genuine_software_names):
        return False

    # If none of the suspicious conditions are met, return False
    return False

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\Prathmesh\Downloads\OC-23-1101-1825-00005241 (3).pdf"

    metadata = extract_pdf_metadata(pdf_file_path)

    print("PDF Metadata:")
    print("------------")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    if is_metadata_suspicious(metadata):
        print("Document is fraudulent due to suspicious metadata.")
    else:
        print("Metadata analysis passed. Proceed to the next stage.")
