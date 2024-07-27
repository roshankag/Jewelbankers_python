from PIL import Image
import google.generativeai as genai
import os
import json
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'

def text_classifier(image_path):
    api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",)
    image = Image.open(image_path)
    response=model.generate_content(["extract name of pawner,extract amount,extra item decription ,extract weight,return in dictionary format",image],stream=False)
    if response.candidates and response.candidates[0].content.parts:
        extracted_text = response.candidates[0].content.parts[0].text
        return json.dumps(extracted_text)
    else:
        return None 




