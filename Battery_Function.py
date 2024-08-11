import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
model = load_model('Battery.h5') 
def predict_battery(model, img_path):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0
    prediction = model.predict(img_array)
    if prediction > 0.5:
        return "Good"
    else:
        return "Bad"