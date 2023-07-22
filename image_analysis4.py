import cv2
import numpy as np
import PyPDF2
import io
import pytesseract
from pytesseract import Output

def extract_images_from_pdf(pdf_file_path):
    images = []
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].get_object()
                    image = data.get_data()
                    image_array = np.frombuffer(image, dtype=np.uint8)
                    image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    images.append((size, image_array))
    return images


def detect_logo_change(image, reference_logo):
    # Convert the image and the reference logo to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_reference_logo = cv2.cvtColor(reference_logo, cv2.COLOR_BGR2GRAY)

    # Initialize the SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors in both the image and the reference logo
    kp_image, des_image = sift.detectAndCompute(gray_image, None)
    kp_reference_logo, des_reference_logo = sift.detectAndCompute(gray_reference_logo, None)

    # Initialize the feature matcher (Brute-Force Matcher)
    bf = cv2.BFMatcher()

    # Match the descriptors of the image and the reference logo
    matches = bf.knnMatch(des_reference_logo, des_image, k=2)

    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Draw the matches on the image
    matching_result = cv2.drawMatches(reference_logo, kp_reference_logo, image, kp_image, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return matching_result, len(good_matches)



if _name_ == "_main_":
    # Load the reference logo from the reference PDF
    reference_pdf_path = r"C:\Users\Srushti Rupapara\Downloads\Health doc\5315416-RADHA TOMAR - CLOSURE REPORT.pdf"  # Replace with the path to your reference PDF
    reference_pdf_images = extract_images_from_pdf(reference_pdf_path)
    
    # Assuming the reference logo is in the first page of the reference PDF
    reference_logo = reference_pdf_images[0][1]

    # Load the PDF file and convert it into images
    pdf_file_path = r"C:\Users\Srushti Rupapara\Downloads\5315416-RADHA TOMAR - CLOSURE REPORT.pdf"  # Replace with the path to your PDF document
    pdf_images = extract_images_from_pdf(pdf_file_path)

    # Analyze each image in the PDF and check for logo forgery
    for idx, (size, image) in enumerate(pdf_images, 1):
        print(f"Analyzing Image {idx}...")
        matching_result, num_good_matches = detect_logo_change(image, reference_logo)

        # Define a threshold for the number of good matches to consider the logo as genuine
        threshold_good_matches = 10  # Adjust this threshold based on your requirements

        if num_good_matches < threshold_good_matches:
            print("Logo appears to be forged or its position is changed.")
        else:
            print("Logo analysis passed. Logo appears to be genuine.")

        # Display the matching result for visualization
        cv2.imshow(f"Matching Result for Image {idx}", matching_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()