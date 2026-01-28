import base64
import easyocr

# Initialize reader once to avoid reloading model
# NOTE: This might download the model on first run
reader = easyocr.Reader(['en'])

async def process_image_input(image_base64: str) -> str:
    """Placeholder for processing base64 encoded image input and extracting text via OCR.
    """
    try:
        # Clean base64 string if it contains header
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,")[1]
            
        decoded_bytes = base64.b64decode(image_base64)
        
        # EasyOCR supports bytes directly
        result = reader.readtext(decoded_bytes, detail=0)
        
        return " ".join(result)
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""
