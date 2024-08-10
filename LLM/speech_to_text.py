import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()["text"]

input = ".\\TEST\\WhatsApp Audio 2024-08-04 at 19.14.35_6aa9df4b.dat.unknown"

output = query(input)
print(output)