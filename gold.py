import yfinance as yf
import json

def get_gold_silver_rates_per_gram():
    gold_ticker = "GC=F"  
    silver_ticker = "SI=F"  

    gold_data = yf.Ticker(gold_ticker).history(period="1d")
    silver_data = yf.Ticker(silver_ticker).history(period="1d")

    gold_price_per_gram_18 = round(gold_data["Close"][0] * 1.2 / 31.1035 * 83.33, 2)  # Adjusting for 18 carat purity and converting to per gram in INR
    gold_price_per_gram_22 = round(gold_data["Close"][0] * 1.3 / 31.1035 * 83.33, 2)  # Adjusting for 22 carat purity and converting to per gram in INR
    gold_price_per_gram_24 = round(gold_data["Close"][0] * 1.4 / 31.1035 * 83.33, 2)  # Adjusting for 24 carat purity and converting to per gram in INR

    silver_price_per_gram = round(silver_data["Close"][0] / 31.1035 * 83.33, 2)  # Converting to per gram in INR

    # Returning as JSON
    result = {
        "gold_rates_per_gram": {
            "18_carat": {
                "rate_INR_per_gram": gold_price_per_gram_18,
            },
            "22_carat": {
                "rate_INR_per_gram": gold_price_per_gram_22,
            },
            "24_carat": {
                "rate_INR_per_gram": gold_price_per_gram_24,
            },
        },
        "silver_rate_per_gram": {
            "rate_INR_per_gram": silver_price_per_gram,
        },
    }

    return json.dumps(result, indent=4)

# Call the function to get the rates per gram
rates_per_gram = get_gold_silver_rates_per_gram()
print(rates_per_gram)
