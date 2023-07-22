import cv2
import PyPDF2
import io
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract installation path

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
                    images.append((size, image))
    return images

def analyze_image_features(image):
    try:
        # Convert image data to a format that OpenCV can read
        image_data = io.BytesIO(image)
        image_array = np.array(Image.open(image_data))

        # Preprocessing: Convert to grayscale and apply better filtering techniques
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        adaptive_threshold_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY, 11, 2)

        # Perform OCR using Tesseract to extract text and font information
        custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode: Default + Page segmentation mode: Assume a single uniform block of text
        text_data = pytesseract.image_to_data(adaptive_threshold_image, config=custom_config, output_type=pytesseract.Output.DICT)

        # Analyze font consistency
        detected_fonts = set(font for font in text_data.get('font', []) if font.strip())

        # If more than one unique font is detected, raise suspicion
        if len(detected_fonts) > 1:
            print("Document is suspicious due to font inconsistency.")
        else:
            print("Font consistency analysis passed. No font inconsistency detected.")

        # Assess image quality
        sharpness, contrast = assess_image_quality(gray_image)

        # Image quality thresholds (computed based on image statistics)
        sharpness_threshold = np.percentile(sharpness, 90)
        contrast_threshold = np.percentile(contrast, 10)

        # Analyze image quality and raise suspicion if thresholds are not met
        if sharpness < sharpness_threshold or contrast < contrast_threshold:
            print("Document is suspicious due to low image quality.")
        else:
            print("Image quality analysis passed. Image quality is acceptable.")

        # Assess lighting conditions and shadows
        brightness, shadow_variance = assess_lighting_and_shadows(gray_image)

        # Lighting and shadows analysis thresholds (computed based on image statistics)
        brightness_threshold = np.percentile(brightness, 95)
        shadow_variance_threshold = np.percentile(shadow_variance, 95)

        # Analyze lighting conditions and shadows and raise suspicion if thresholds are not met
        if brightness < brightness_threshold or shadow_variance < shadow_variance_threshold:
            print("Document is suspicious due to unusual lighting or shadows.")
        else:
            print("Lighting and shadows analysis passed. Lighting conditions and shadows are acceptable.")

        coverage_percentage = detect_artifacts_along_edges(image_array)

        # Artifacts along document edges analysis threshold (computed based on image statistics)
        coverage_threshold = np.percentile(coverage_percentage, 90)

        # Analyze artifacts along document edges and raise suspicion if the coverage percentage is high
        if coverage_percentage > coverage_threshold:
            print("Document is suspicious due to artifacts along document edges.")
        else:
            print("Artifacts along document edges analysis passed. No significant artifacts detected.")

    except Exception as e:
        print(f"Error: {e}")

def assess_image_quality(image):
    # Calculate the image sharpness using Laplacian variance
    sharpness = cv2.Laplacian(image, cv2.CV_64F).var()

    # Calculate the image contrast using the standard deviation of pixel intensities
    contrast = np.std(image.flatten())

    return sharpness, contrast

def assess_lighting_and_shadows(image):
    # Calculate the image brightness
    brightness = image.mean()

    # Calculate the image variance to assess the level of shadow
    _, threshold_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    shadow_variance = cv2.Laplacian(threshold_image, cv2.CV_64F).var()

    return brightness, shadow_variance

def detect_artifacts_along_edges(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform Canny edge detection to find edges in the image
    edges = cv2.Canny(gray_image, 100, 200)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the perimeter of the document bounding box
    max_perimeter = 0
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        if perimeter > max_perimeter:
            max_perimeter = perimeter

    # Calculate the area of the document bounding box
    area = max_perimeter ** 2 / (4 * 3.1416)

    # Calculate the area of the entire image
    image_area = image.shape[0] * image.shape[1]

    # Calculate the percentage of the image covered by the document bounding box
    coverage_percentage = (area / image_area) * 100

    return coverage_percentage




if __name__ == "_main_":
    pdf_file_path = r"C:\Users\Yash\Downloads\Amazon 1.pdf"  # Replace with the actual PDF file path
    pdf_images = extract_images_from_pdf(pdf_file_path)
    for idx, (size, image) in enumerate(pdf_images, 1):
        print(f"Analyzing Image {idx}...")
        analyze_image_features(image)