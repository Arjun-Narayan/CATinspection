from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
model = load_model('CNN Tire Texture Classification.h5') 
def predict_tire(model, img_path):
  img = image.load_img(img_path, target_size=(379, 379), color_mode = "grayscale")
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  img_array /= 255.0 
  prediction = model.predict(img_array)
  if prediction[0][0] > 0.5:
    return "Cracked"
  else:
    return "Normal"
loaded_model = load_model('CNN Tire Texture Classification.h5')
image_path = '../input/tire-texture-image-recognition/Tire Textures/testing_data/cracked/Cracked_001.jpg'  # Replace with the actual image path
result = predict_tire(loaded_model, image_path)
print(f"The tire is predicted to be: {result}")