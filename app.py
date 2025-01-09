import flask
import easyocr
 
def extract_text_from_image(image_path):
    """
    Extract text from the given image using EasyOCR.
    """
    # Initialize the EasyOCR Reader
    reader = easyocr.Reader(['en'])  # You can add more languages if needed
 
    # Perform OCR on the image
    results = reader.readtext(image_path)
 
    # Combine all detected text into a single string
    extracted_text = " ".join([text[1] for text in results])
    return extracted_text
 
def verify_details(extracted_text, user_details):
    """
    Verify extracted text against user-provided details.
    """
    verification_results = {}
    for field, value in user_details.items():
        if value.lower() in extracted_text.lower():
            verification_results[field] = "Verified"
        else:
            verification_results[field] = "Not Verified"
    return verification_results
 
if __name__ == "__main__":
    # Input: Image path of the RC document
    rc_image_path = "C:/Users/lamtu/Downloads/image_.jpeg"  # Replace with your image path
 
    # User-provided details to verify
    user_provided_details = {
        "Owner Name": "Harsh Bailurkar",  # Replace with the actual name
        "Vehicle Number": "MH 09 BE 2025",  # Replace with the actual number plate
        "Vehicle Model": "Zen",  # Replace with the actual vehicle model
    }
 
    # Step 1: Extract text from the RC image
    extracted_text = extract_text_from_image(rc_image_path)
    print("Extracted Text from RC Document:")
    print(extracted_text)
 
    # Step 2: Verify details
    verification_results = verify_details(extracted_text, user_provided_details)
 
    # Step 3: Display verification results
    print("\nVerification Results:")
    for field, status in verification_results.items():
        print(f"{field}: {status}")