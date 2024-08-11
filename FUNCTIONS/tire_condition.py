import sys
import io
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


model = load_model('./MODEL/CNN Tire Texture Classification.h5') 
model.compile(optimizer='adam', loss='binary_crossentropy')

def predict_tire(model, img_path):
    img = image.load_img(img_path, target_size=(379, 379), color_mode="grayscale")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0 
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:
        return "Bad"
    else:
        return "Good"
