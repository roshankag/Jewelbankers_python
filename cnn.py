from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import jellyfish
import re
from  genai2 import text_classifier
def similarity_score_jellyfish(str1, str2):
    str1=str1.lower()
    str2=str2.lower()
    cleaned_text1 = re.sub(r'\b(?:s/o|d/o|c/o|w/o)\b', '', str1, flags=re.IGNORECASE)
    cleaned_text1 = re.sub(r'\s+', ' ', cleaned_text1).strip()
    cleaned_text2 = re.sub(r'\b(?:s/o|d/o|c/o|w/o)\b', '', str2, flags=re.IGNORECASE)
    cleaned_text2 = re.sub(r'\s+', ' ', cleaned_text2).strip()
    score = jellyfish.jaro_winkler_similarity(cleaned_text1,cleaned_text2)
    return score

def name(str1):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='deepak',  
            user='root', 
            password='Deepak@2005'  
        )

        if conn.is_connected():
            cursor = conn.cursor()
            query = 'select customername from deepak.customer'
            cursor.execute(query)
            rows=cursor.fetchall()
            customer_names = ',\n '.join([row[0] for row in rows])
            conn.commit()
            cursor.close()
            conn.close()
            customer_names=[]
            for i in rows :
                  example_string = str(i)
                  cleaned_string = example_string.strip("(),'")
                  customer_names.append(cleaned_string)
            prediction={}
            for i in customer_names:
                a=similarity_score_jellyfish(i,str1)
                prediction[i]=a
            max_key = max(prediction, key=prediction.get)
            max_value = prediction[max_key]
            return prediction
        else:
              print('not done')

    except Error as e:
        print('exception')

# import json
# Image1=r"C:\Users\deepa\Downloads\sample bill.jpg"
# json_string=text_classifier(Image1)
# cleaned_string = json_string.strip('"').strip('```json\n').strip('\n```')
# data = json.loads(cleaned_string)
# print(data['name_of_pawner'])


str1='Bhaskar G.Munnayay'

scores=name(str1)
for key, value in scores.items():
    if value >0.80:
        print(f"{key}: {value}")