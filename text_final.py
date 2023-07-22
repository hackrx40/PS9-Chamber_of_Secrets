import PyPDF2
import os
import re

def extract_id_and_fir_no(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Extract Payment Transaction ID
        payment_match = re.search(r'Payment Transaction ID: (\S+)', text)
        payment_id = payment_match.group(1) if payment_match else None

        # Extract FIR No
        fir_match = re.search(r'FIR Number: (\S+)', text)
        fir_no = fir_match.group(1) if fir_match else None

        return payment_match, payment_id, fir_match, fir_no

def check_fraud(directory, target_id):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            payment_match, payment_id, fir_match, fir_no = extract_id_and_fir_no(file_path)
            if payment_id == target_id:
                return True, filename, payment_id, "PAY"
            elif fir_no == target_id:
                return True, filename, fir_no, "FIR"
    return False, None, None, None

def main():
    file_path = r"C:\Users\Prathmesh\Downloads\Amazon 2 F sign.pdf"
    payment_match, target_id, fir_match, target_fir_no = extract_id_and_fir_no(file_path)
    print(f'Payment Transaction ID: {target_id}')
    print(f'FIR No: {target_fir_no}')

    if target_id is not None:
        if fir_match and fir_match.group(0).startswith('FIR'):
            directory = r"C:\Users\Prathmesh\Downloads\New folder (4)\FIR"  # Directory for FIR No search
        elif payment_match and payment_match.group(0).startswith('Payment'):
            directory = r"C:\Users\Prathmesh\Downloads\New folder (4)\invoice"  # Directory for Payment Transaction ID search
        else:
            print('Invalid keyword extracted from the document.')
            return

        is_fraud, fraud_file, fraud_id, id_prefix = check_fraud(directory, target_id)
        if is_fraud:
            print(f'Fraud detected in file: {fraud_file}')
        else:
            print('No fraud detected.')

if __name__ == '__main__':
    main()
