import requests  # For making API calls
import re
import jellyfish

def similarity_score_jellyfish(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    # Remove specific prefixes and extra whitespace
    cleaned_text1 = re.sub(r'\b(?:s/o|d/o|c/o|w/o)\b', '', str1, flags=re.IGNORECASE)
    cleaned_text1 = re.sub(r'\s+', ' ', cleaned_text1).strip()
    cleaned_text2 = re.sub(r'\b(?:s/o|d/o|c/o|w/o)\b', '', str2, flags=re.IGNORECASE)
    cleaned_text2 = re.sub(r'\s+', ' ', cleaned_text2).strip()
    # Calculate similarity score
    score = jellyfish.jaro_winkler_similarity(cleaned_text1, cleaned_text2)
    return score

def fetch_customer_names_from_api(api_url, token):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        data = response.json()
        #print("API response data:", data)  # Print data to inspect the structure

        # Assuming data is a list or has a different structure, adjust here:
        if isinstance(data, list):
            # If data is a list of customers
            customer_names = [customer["customerName"] for customer in data]
        elif isinstance(data, dict) and "customer" in data:
            # If 'customer' is a key in the dictionary data
            customer_names = [customer["customerName"] for customer in data["customer"]]
        else:
            #print("Unexpected data format")
            return []  # Return an empty list if format is unexpected

        return customer_names

    except requests.exceptions.RequestException as e:
        #print("API request error:", e)
        return []  # Return an empty list if there's an error

def find_best_match(str1, api_url, token):
    # Fetch customer names from the API
    customer_names = fetch_customer_names_from_api(api_url, token)
    prediction = {}
    
    # Calculate similarity score for each customer name
    for customer_name in customer_names:
        score = similarity_score_jellyfish(customer_name, str1)
        prediction[customer_name] = score

    # Find the best match
    if prediction:
        max_key = max(prediction, key=prediction.get)
        max_value = prediction[max_key]
        
        # Check if the top score is below 0.4
        if max_value < 0.4:
            return str1, max_value  # Return the input name and the score
        
        return max_key, max_value  # Return the top match with the highest score
    else:
        return str1, 0  # If no matches found, return the input name with score 0


