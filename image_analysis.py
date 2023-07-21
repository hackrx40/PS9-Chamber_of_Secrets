import PyPDF2
import difflib

def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def compare_pdf_text(reference_pdf_path, forged_pdf_path):
    reference_text = extract_text_from_pdf(reference_pdf_path)
    forged_text = extract_text_from_pdf(forged_pdf_path)

    seq_matcher = difflib.SequenceMatcher(None, reference_text, forged_text)
    similarity_score = seq_matcher.ratio()
    return similarity_score

# Replace 'reference_pdf.pdf' and 'forged_pdf.pdf' with the actual file paths of the reference and forged PDFs.
reference_pdf_path = r"C:\Users\Prathmesh\Downloads\Forgery document use case\Forgery document use case\Hackathon\invoice\Amazon 2.pdf"
forged_pdf_path = r"C:\Users\Prathmesh\Downloads\Amazon 2 F sign.pdf"

similarity_score = compare_pdf_text(reference_pdf_path, forged_pdf_path)
print(f"Similarity Score: {similarity_score}")