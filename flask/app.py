# app.py
from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            pdf_reader = PyPDF2.PdfReader(file)
            doc_info = pdf_reader.metadata
            metadata = {
                "Title": doc_info.get("/Title", None),
                "Author": doc_info.get("/Author", None),
                "Subject": doc_info.get("/Subject", None),
                "Producer": doc_info.get("/Producer", None),
                "Creator": doc_info.get("/Creator", None),
                "PageCount": len(pdf_reader.pages)
            }
            return render_template('display.html', metadata=metadata)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
