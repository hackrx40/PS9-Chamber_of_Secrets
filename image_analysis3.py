import os
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

def compare_pdf_text(reference_text, forged_pdf_path_list):
    similarity_scores = {}
    for pdf_path in forged_pdf_path_list:
        forged_text = extract_text_from_pdf(pdf_path)

        seq_matcher = difflib.SequenceMatcher(None, reference_text, forged_text)
        similarity_score = seq_matcher.ratio()
        similarity_scores[os.path.basename(pdf_path)] = similarity_score
    return similarity_scores

if __name__ == "__main__":
    reference_pdf_path = r"C:\Users\Prathmesh\Downloads\Amazon 2 F sign.pdf"
    forged_pdf_folder_path = r"C:\Users\Prathmesh\Downloads\New folder (4)\invoice"  # Replace with the path to the folder containing PDFs

    # Extract text from the reference PDF
    reference_text = extract_text_from_pdf(reference_pdf_path)

    # Get the list of PDF files from the folder
    pdf_files = [file for file in os.listdir(forged_pdf_folder_path) if file.endswith(".pdf")]
    forged_pdf_path_list = [os.path.join(forged_pdf_folder_path, file) for file in pdf_files]

    # Compare the text of the reference PDF with each PDF in the folder
    similarity_scores = compare_pdf_text(reference_text, forged_pdf_path_list)

    # Print similarity scores
    for pdf_file, similarity_score in similarity_scores.items():
        print(f"{pdf_file}: Similarity Score - {similarity_score}")
