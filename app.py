from flask import Flask, request, jsonify
import easyocr
import requests
from io import BytesIO
from PIL import Image
from flask_cors import CORS
import os
import tempfile

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
    """
    Extract text from the given image using EasyOCR.
    """
    # Open the image
    image = Image.open(image_path)

    # Perform OCR on the image
    results = reader.readtext(image)

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

@app.route("/verify", methods=["POST"])
def verify():
    """
    API endpoint to verify RC details from an image.
    """
    try:
        # Get the data from the request body
        user_data = request.form.to_dict()
        image_file = request.files.get("imgUrl")

        if not image_file or not user_data:
            return jsonify({"error": "Missing imgUrl or userData in request body"}), 400

        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image_file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Step 1: Extract text from the image
        extracted_text = extract_text_from_image(temp_file_path)
        
        # Step 2: Verify details
        verification_results = verify_details(extracted_text, user_data)

        verified = False
        if(verification_results['Owner Name'] == 'Verified' and verification_results['Vehicle Number'] == 'Verified'  ):
            verified = True
        else:
            verified = False

        # Delete the temporary file
        os.remove(temp_file_path)

        # Return the results as a JSON response
        return jsonify({
            "verified": verified,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
