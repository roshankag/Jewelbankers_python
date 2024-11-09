import json
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import uvicorn
from cnn import find_best_match
from genai2 import text_classifier
from speech21 import speech

# Create FastAPI instance
app = FastAPI()


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to process speech data
# @app.post("/customer")
# async def get_customer(input_data: Input):
#     try:
#         # Call the speech processing function
#         result = speech(input_data.input)  # Replace with your actual function
#         return {"message": "Processed speech data", "data": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")

class Input(BaseModel):
    input: str  # The input string from the frontend
    token: str  # The token provided by the frontend for authentication

@app.post("/customer")
async def get_customer(input_data: Input):
    try:
        # Log the input data and token
        print(f"Received input: {input_data.input}")
        print(f"Received token: {input_data.token}")

        # Call the speech processing function with the input and token
        result = speech(input_data.input, input_data.token)  # Your processing function that needs the input and token

        return {"message": "Processed speech data", "data": result}
    except Exception as e:
        print(f"Error processing customer input: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")  # Return a 500 error if something goes wrong


# Endpoint to fetch gold and silver rates
@app.get("/rates")
async def get_rates():
    try:
        result = {"gold_rate": 5000, "silver_rate": 100}  # Replace with your actual function
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to upload an image and process it


# Root endpoint for debugging speech
@app.post("/")
async def debug_customer(input_data: Input):
    return {"message": "Debug processed", "input": input_data.input}

@app.post("/image")
async def upload_image_for_classification(file: UploadFile = File(...), token: str = Form(...)):
    try:
        image_data = await file.read()

        # Assuming text_classifier processes the image and returns the result
        result = text_classifier(image_data)

        # Debugging: print result to verify its format
        print(f"Result from text_classifier: {result}")

        # Step 1: Remove all newline characters and clean up escape characters
        cleaned_result = result.replace('\n', '')  # Remove all newline characters
        cleaned_result = re.sub(r'\\"', '"', cleaned_result)  # Remove extra backslashes
        cleaned_result = cleaned_result.strip('"')  # Remove outer quotes

        # Debugging: print cleaned result to check if newlines are properly removed
        print(f"Cleaned Result: {cleaned_result}")
        len2=len(cleaned_result)

        # Step 2: Parse the cleaned result into JSON
        try:
            parsed_result = json.loads(cleaned_result[:len2-2])  # Parse into dictionary
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return JSONResponse(content={"error": f"JSON decoding error: {e}"}, status_code=500)

        # Step 3: Build the response object
        response = {
            "need": parsed_result.get("need", None),
            "customer_name": parsed_result.get("customer_name", None),
            "weight": parsed_result.get("weight", None),
            "article": parsed_result.get("article", None),
            "amount": parsed_result.get("amount", None),
            "item_description": parsed_result.get("item_description", None),
            "billnumber": {
                "bill_serial": parsed_result.get("billnumber", {}).get("bill_serial", None),
                "bill_number": parsed_result.get("billnumber", {}).get("bill_number", None)
            },
            "print_details": None  # Assuming this is an additional field you may need
        }
        api_url = 'http://localhost:8080/jewelbankersapi/customers?customerName' 

        # Check if 'customer_name' exists in response_json
        if 'customer_name' in response:
            best_match_name, best_match_score = find_best_match(response['customer_name'], api_url, token)
            response['customer_name'] = best_match_name  # Update the customer_name in the JSON response
            print("response final",response)
        return response  # Returning the formatted response

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)