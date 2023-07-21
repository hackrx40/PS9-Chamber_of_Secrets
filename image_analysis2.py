import cv2
import PyPDF2
import io
import numpy as np
import pytesseract
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
        image_array = cv2.imdecode(np.frombuffer(image_data.read(), dtype=np.uint8), 1)

        # Check if the image was successfully loaded
        if image_array is None:
            print("Error: Failed to load image.")
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Preprocessing: Convert to grayscale
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract to extract text and font information
    custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode: Default + Page segmentation mode: Assume a single uniform block of text
    text_data = pytesseract.image_to_data(gray_image, config=custom_config, output_type=pytesseract.Output.DICT)

    # Analyze font consistency
    detected_fonts = set()
    if 'font' in text_data:
        for i in range(len(text_data['text'])):
            text = text_data['text'][i].strip()
            font = text_data['font'][i] if i < len(text_data['font']) else None

            if text and font:
                detected_fonts.add(font)

    # If more than one unique font is detected, raise suspicion
    if len(detected_fonts) > 1:
        print("Document is suspicious due to font inconsistency.")
    else:
        print("Font consistency analysis passed. No font inconsistency detected.")

        
    # Assess image quality
    sharpness, contrast = assess_image_quality(image_array)

    # Image quality thresholds (you can adjust these values based on your requirements)
    sharpness_threshold = 100.0
    contrast_threshold = 30.0

    # Analyze image quality and raise suspicion if thresholds are not met
    if sharpness < sharpness_threshold or contrast < contrast_threshold:
        print("Document is suspicious due to low image quality.")
    else:
        print("Image quality analysis passed. Image quality is acceptable.")

    # Assess lighting conditions and shadows
    brightness, shadow_variance = assess_lighting_and_shadows(image_array)

    # Lighting and shadows analysis thresholds (you can adjust these values based on your requirements)
    brightness_threshold = 100  # Adjust as needed
    shadow_variance_threshold = 1000  # Adjust as needed

    # Analyze lighting conditions and shadows and raise suspicion if thresholds are not met
    if brightness < brightness_threshold or shadow_variance < shadow_variance_threshold:
        print("Document is suspicious due to unusual lighting or shadows.")
    else:
        print("Lighting and shadows analysis passed. Lighting conditions and shadows are acceptable.")
    
    coverage_percentage = detect_artifacts_along_edges(image_array)

    # Artifacts along document edges analysis threshold (you can adjust this value based on your requirements)
    coverage_threshold = 90.0  # Adjust as needed

    # Analyze artifacts along document edges and raise suspicion if the coverage percentage is high
    if coverage_percentage > coverage_threshold:
        print("Document is suspicious due to artifacts along document edges.")
    else:
        print("Artifacts along document edges analysis passed. No significant artifacts detected.")
    
    # Display the original image and/or the analysis results (if needed)
    cv2.imshow("Original Image", image_array)
    cv2.imshow("Grayscale Image", gray_image)

    # Wait for a key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def assess_image_quality(image):
    # Calculate the image sharpness using Laplacian variance
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray_image, cv2.CV_64F).var()

    # Calculate the image contrast using the standard deviation of pixel intensities
    pixel_values = gray_image.flatten()
    contrast = np.std(pixel_values)

    return sharpness, contrast

def assess_lighting_and_shadows(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the image brightness
    brightness = gray_image.mean()

    # Calculate the image variance to assess the level of shadow
    _, threshold_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
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

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\Prathmesh\Downloads\Amazon 1 F.pdf"  # Replace with the actual PDF file path
    pdf_images = extract_images_from_pdf(pdf_file_path)
    for idx, (size, image) in enumerate(pdf_images, 1):
        print(f"Analyzing Image {idx}...")
        analyze_image_features(image)