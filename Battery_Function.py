import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
model=tf.lite.Interpreter(model_path="Battery.tfile")
model.allocate_tensors()
input_details=model.get_input_details()
output_details=model.get_output_details()
def predict_battery(model, img_path):
    img=image.load_img(img_path, target_size=(150, 150))
    img_array=image.img_to_array(img)
    img_array=np.expand_dims(img_array, axis=0)
    img_array /= 255.0 
    model.set_tensor(input_details[0]['index'], img_array)
    model.invoke()
    prediction=model.get_tensor(output_details[0]['index'])
    if prediction[0] > 0.5:
        return "Good"
    else:
        return "Bad"
