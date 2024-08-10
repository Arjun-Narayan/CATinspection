import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

model = load_model('.\MODELS\\tire_pressure_model.h5') 

def classify_tire(image_path, model):
    # Load the image and preprocess it
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0 

    # Make predictions
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions)
    
    # Map the index to the class label
    class_names = ['flat', 'full', 'no-tire']
    return class_names[class_idx]


result = classify_tire('.\\TEST\\00000.jpg', model)
print("The tire is:", result)