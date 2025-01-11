# RC Verification for Uber

This project is a Flask application that verifies RC (Registration Certificate) details from an uploaded image using EasyOCR.

## Requirements

- Python 3.x
- Flask==2.0.1
- easyocr==1.4
- requests==2.25.1
- Pillow==8.2.0
- gunicorn==20.1.0
- flask_cors==3.0.10
- tempfile

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd RC_verification_for_Uber
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask app:
    ```sh
    python app.py
    ```

2. The app will be available at `http://localhost:5000`.

## API Endpoints

### POST /verify

This endpoint verifies RC details from an uploaded image.

#### Request

- `Content-Type: multipart/form-data`
- Form Data:
  - `imgUrl`: The image file containing the RC details.
  - Other form fields representing user details to be verified.

#### Response

- `200 OK` on success:
    ```json
    {
        "verified": true
    }
    ```
- `400 Bad Request` if `imgUrl` or user data is missing:
    ```json
    {
        "error": "Missing imgUrl or userData in request body"
    }
    ```
- `500 Internal Server Error` on failure:
    ```json
    {
        "error": "<error_message>"
    }
    ```

## Functions

### extract_text_from_image(image_path)

Extracts text from the given image using EasyOCR.

### verify_details(extracted_text, user_details)

Verifies extracted text against user-provided details.

## License

This project is licensed under the MIT License.
