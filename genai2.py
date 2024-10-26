# text_classifier.py
from PIL import Image
import google.generativeai as genai
import os
import json
import io

# Load API key from environment variables


# Set up the API configuration
genai.configure(api_key=os.getenv('GENAI_API_KEY'))

def text_classifier(image_data):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
        
        # Open the image from the byte stream
        image_stream = io.BytesIO(image_data)
        image = Image.open(image_stream)
        
        # Generate content from the image
        response = model.generate_content(
            ["""If the need is "pledge", return JSON with:

need: "pledge"
customer_name: (string, if available)
weight: (float, if available, extracted from the left side of the paper under the weight column)
article: (string, auto-filled based on item_description)
item_description: (string, extracted from the box below the bill number, if available)
amount: (integer, if available)
The article should be filled as follows:

If item_description contains 'gold', set article to 'gold'.
If item_description contains 'silver', set article to 'silver'.
Otherwise, set article to 'ornament'.
The bill number is located at the top right of the photo. The first part will be considered the bill_serial, followed by the remaining part, which will be the bill_number (five digits down from the bill serial). The customer name should be extracted from below the bill number, if present.

If the need is "redeem", return JSON with:

need: "redeem"
billnumber:
bill_serial: (string, alphabet present before the bill number, extracted as described above)
bill_number: (string, if available, extracted from the same location)
If the need is "search", return JSON with:

need: "search"
customer_name: (string, if available, extracted as specified)
bill_number: (string, if available, extracted as specified)
If the need is "print", return JSON with:

need: "print"
print_details: (string, details to be specified based on the context of the print operation)
If there is no proper text, supply all values as null, and ensure the bill_serial is the alphabet present before the bill_number.
             Return the JSON in the following format:
{
  "need": str,
  "customer_name": str (optional),
  "weight": float (optional),
  "article": str (optional),
  "amount": int (optional),
  "item_description": str (optional),
  "billnumber": {
    "bill_serial": str (optional),
    "bill_number": str (optional)
  },
  "print_details": str (optional)
}""", image],
            stream=False
        )
        
        if response.candidates and response.candidates[0].content.parts:
            extracted_text = response.candidates[0].content.parts[0].text
            return json.dumps(response.text)
        else:
            return json.dumps({"error": "No content found"})
    except Exception as e:
        return json.dumps({"error": str(e)})
    
