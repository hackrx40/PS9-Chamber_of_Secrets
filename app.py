from flask import Flask, render_template, request
import os
import meta  # Import the provided Python files
import text
import image
import logo

app = Flask(__name__)

# Ensure the 'tmp' directory exists
if not os.path.exists('tmp'):
    os.makedirs('tmp')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return "No PDF file provided."

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file."

    # Save the uploaded PDF file temporarily to the 'tmp' folder
    pdf_path = os.path.join('tmp', pdf_file.filename)
    pdf_file.save(pdf_path)

    # Perform the analysis and store results in a dictionary
    results = {}

    metadata = meta.extract_pdf_metadata(pdf_path)
    results['Metadata Analysis'] = "Fraudulent" if meta.is_metadata_suspicious(metadata) else "Not Fraudulent"

    payment_match, target_id, fir_match, target_fir_no = text.extract_id_and_fir_no(pdf_path)
    if fir_match and fir_match.group(0).startswith('FIR'):
        directory = r"C:\Users\Prathmesh\Downloads\New folder (4)\FIR"  # Directory for FIR No search
    elif payment_match and payment_match.group(0).startswith('Payment'):
        directory = r"C:\Users\Prathmesh\Downloads\New folder (4)\invoice"  # Directory for Payment Transaction ID search
    else:
        results['Text Analysis'] = 'Invalid keyword extracted from the document.'
        return render_template('result.html', results=results)

    is_fraud, fraud_file, fraud_id, id_prefix = text.check_fraud(directory, target_id)
    if is_fraud:
        results['Text Analysis'] = f'Fraud detected in file: {fraud_file}'
    else:
        results['Text Analysis'] = 'No fraud detected.'

    pdf_images = image.extract_images_from_pdf(pdf_path)
    for idx, (_, image) in enumerate(pdf_images, 1):
        matching_result, num_good_matches = image.detect_logo_change(image, logo.reference_logo)
        threshold_good_matches = 10  # Adjust this threshold based on your requirements
        if num_good_matches < threshold_good_matches:
            results[f'Image Analysis {idx}'] = "Logo appears to be forged or its position is changed."
        else:
            results[f'Image Analysis {idx}'] = "Logo analysis passed. Logo appears to be genuine."

    # Render the results in the result.html template
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
