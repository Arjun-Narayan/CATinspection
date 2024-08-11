import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

def query(filename):
    API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
    headers = {"Authorization": f"Bearer {hugging_face_api_key}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def query2(payload):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {hugging_face_api_key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def value_filler_tires(input_text, template, character_limit=900):
    chunks = [input_text[i:i+character_limit] for i in range(0, len(input_text), character_limit)]
    full_output = ""
    
    for i, chunk in enumerate(chunks):
        payload = {
            "inputs": template + chunk,
            "parameters": {
                "return_full_text": False
            }
        }

        output = query2(payload)
        if isinstance(output, list) and len(output) > 0:
            full_output += output[0].get('generated_text', '')

    return full_output.replace("▪", "-")  

def voice_assistant_tire(file_path):
    speech = query(file_path)
    input_text = speech.get('text', '')


    template = """From the Given Text create the report according to the given template:
        - Tire Pressure for Left Front:
        - Tire Pressure for Right Front:
        - Tire Condition for Left Front: (Good, Ok, Needs Replacement)
        - Tire Condition for Right Front: (Good, Ok, Needs Replacement)
        - Tire Pressure for Left Rear:
        - Tire Pressure for Right Rear:
        - Tire Condition for Left Rear: (Good, Ok, Needs Replacement)
        - Tire Condition for Right Rear: (Good, Ok, Needs Replacement)
    """

    output = value_filler_tires(input_text, template)
    return output

input_path = ".\\TEST\\tire.dat.unknown"
print(voice_assistant_tire(input_path))