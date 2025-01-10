from flask import Flask, request, jsonify
import easyocr
import requests
from io import BytesIO
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path_or_url):
    """
    Extract text from the given image using EasyOCR.
    """
    # If the input is a URL, download the image
    if image_path_or_url.startswith("http"):
        response = requests.get(image_path_or_url)
        image = Image.open(BytesIO(response.content))
    else:
        # If it's a local file path, open the image
        image = Image.open(image_path_or_url)

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
        data = request.get_json()
        image_url = data.get("imgUrl")  # URL or file path to the image
        user_data = data.get("userData")  # User details as a dictionary

        if not image_url or not user_data:
            return jsonify({"error": "Missing imgUrl or userData in request body"}), 400

        # Step 1: Extract text from the image
        extracted_text = extract_text_from_image(image_url)
        
        # Step 2: Verify details
        verification_results = verify_details(extracted_text, user_data)

        verified = False
        if(verification_results['Owner Name'] == 'Verified' and verification_results['Vehicle Number'] == 'Verified' and verification_results['Vehicle Model'] == 'Verified' ):
            verified = True
        else:
            verified = False


        # Return the results as a JSON response
        return jsonify({
            "verified": verified,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
    # To run with gunicorn, use the following command:
    # gunicorn app:app
