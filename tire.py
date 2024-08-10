import numpy as np
import os
import tensorflow as tf
import pandas as pd
from fastai import *
from fastai.vision.all import *
from tensorflow.keras.preprocessing import image_dataset_from_directory
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

path = Path('.\DATASETS\\tire-dataset')
dls = ImageDataLoaders.from_folder(path, valid_pct=0.2, item_tfms=Resize(224), bs=80)
img_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                            brightness_range=(0.5,1), 
                            channel_shift_range=0.2,
                            rescale=1./255,
                            validation_split=0.3)
img_generator_flow_train = img_generator.flow_from_directory(
    directory=path,
    target_size=(224, 224),
    batch_size=16,
    shuffle=True,
    subset="training")

img_generator_flow_valid = img_generator.flow_from_directory(
    directory=path,
    target_size=(224, 224),
    batch_size=16,
    shuffle=True, 
    subset="validation") 

#Create the model
model = keras.Sequential([
    layers.InputLayer(input_shape=[224,224,3]),
    layers.RandomContrast(factor=0.10),
    layers.RandomFlip(mode='horizontal'),
    layers.RandomRotation(factor=0.10),
    layers.BatchNormalization(),
    layers.Conv2D(filters=64,kernel_size=3,activation='relu',padding='same'),
    layers.MaxPool2D(),

    layers.BatchNormalization(),
    layers.Conv2D(filters=128,kernel_size=3,activation='relu',padding='same'),
    layers.MaxPool2D(),
    
    layers.BatchNormalization(),
    layers.Conv2D(filters=256,kernel_size=3,activation='relu',padding='same'),
    layers.Conv2D(filters=256,kernel_size=3,activation='relu',padding='same'),
    layers.MaxPool2D(),
    
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(8,activation='relu'),
    layers.Dense(3,activation='sigmoid')
    
])

#Accuracy and loss
optimizer = tf.keras.optimizers.Adam(epsilon=0.01)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics = ['categorical_accuracy']
)

#Train the model
history = model.fit(
    img_generator_flow_train,
    validation_data = img_generator_flow_valid,
    epochs=5
) 

model.save('.\\MODELS\\tire_pressure_model.h5')
history_frame = pd.DataFrame(history.history)
print(pd.DataFrame.head)