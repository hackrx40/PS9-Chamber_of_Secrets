import PyPDF2
import os
import re

def extract_id(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        match = re.search(r'Payment Transaction ID: (\S+)', text)
        if match:
            return match.group(1)
        else:
            return None

def check_fraud(directory, target_id):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            current_id = extract_id(os.path.join(directory, filename))
            if current_id == target_id:
                return True, filename
    return False, None

def main():
    directory = 'C:/Users/Prathmesh/Downloads/New folder (4)/invoice'
    target_file = "C:/Users/Prathmesh/Downloads/Amazon 2 F sign.pdf"
    target_id = extract_id(target_file)
    print(f'Payment Transaction ID: {target_id}')
    if target_id is not None:
        is_fraud, fraud_file = check_fraud(directory, target_id)
        if is_fraud:
            print(f'Fraud detected in file: {fraud_file}')
        else:
            print('No fraud detected.')
    else:
        print('Payment Transaction ID not found in the uploaded PDF.')

if __name__ == '__main__':
    main()
