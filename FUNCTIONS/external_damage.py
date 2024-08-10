import sys
import io
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def classify_image(img_path):
    model = load_model('./MODEL/exterior.h5')  
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    pred = model.predict(img_array)
    pred_class = np.argmax(pred, axis=1)

    known_classes = {
        0: 'bumper_dent',
        1: 'bumper_scratch',
        2: 'door_dent',
        3: 'door_scratch',
        4: 'glass_shatter',
        5: 'head_lamp'
    }

    if pred_class[0] in known_classes:
        classification = known_classes[pred_class[0]]
        result = ["yes", classification]
    else:
        result = ["no"]

    return result
