import json
from fastapi import HTTPException
import google.generativeai as genai
import os
import json

from cnn import find_best_match 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.getenv('GOOGLE_APPLICATION_CREDENTIALS_NEW')
prompt= """
  Given the need, generate a JSON response based on the following conditions:
 
  1. If the need is "pledge", return JSON with:
     - need
     - customer_name
     - weight
     - article (auto-filled based on item_description includesornaments (gold,silver,bronze etc...fill with samll letter))
     - item_description
     - amount
  
     The article should be filled as follows:
     - If item_description contains 'gold', set article to 'gold'.
     - If item_description contains 'silver', set article to 'silver'.
     - Otherwise, set article to 'ornament'.

  2. If the need is "redeem", return JSON with:
     - billnumber
       - bill_serial
       - bill_number

  3. If the need is "search", return JSON with:
     - customer_name
     - bill_number
     - Combine any additional details like amount, material type, or action into a single others field in JSON format, separating multiple items with spaces, e.g., "6000 rs gold redeemed", and ensure all unique items are included without duplicates.

  4. If the need is "print", return JSON with:
     - print_details (details to be specified based on the context of the print operation)
  if there is no proper text supply all value as null and bill serial is the alphabet present before the bill number 
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
    "print_details": str (optional) ,
    "others:str(optional)"
  }
  
"""
def speech(inp,token):
    api_key=os.getenv('GENAI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
    response=model.generate_content(prompt+inp)
    api_url = 'http://localhost:8080/jewelbankersapi/customers?customerName' 

    try:
        response_json = json.loads(response.text)

        # Check if 'customer_name' exists and is not None
        if response_json.get('customer_name'):
            # For 'search' need, extract first alphabetical word before a space
            if response_json.get('need') == 'search':
                customer_name = response_json['customer_name']
                # Extract all alphabetic characters up to the first space
                extracted_name = ''.join(filter(str.isalpha, customer_name.split()[0]))
                # Find best match based on the extracted name
                best_match_name, best_match_score = find_best_match(extracted_name, api_url, token)
                response_json['customer_name'] = best_match_name
            else:
                # For 'redeem' or other needs, directly match customer_name without modifications
                best_match_name, best_match_score = find_best_match(response_json['customer_name'], api_url, token)
                response_json['customer_name'] = best_match_name
        print(response_json)
        return response_json

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Error processing customer input: {str(e)}")


