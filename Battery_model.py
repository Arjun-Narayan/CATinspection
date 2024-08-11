import os
import shutil
dataset_path_in_drive = '/content/drive/MyDrive/dataset'
dataset_path_in_colab = '/content/Untitled Folder'
if os.path.exists(dataset_path_in_colab):
    shutil.rmtree(dataset_path_in_colab)
shutil.copytree(dataset_path_in_drive, dataset_path_in_colab)
print(os.listdir(dataset_path_in_colab))
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
img_folder_good = '/content/Untitled Folder/good'
img_folder_bad = '/content/Untitled Folder/bad'
for filename in os.listdir(img_folder_good): 
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        image_path = os.path.join(img_folder_good, filename) 
        img = mpimg.imread(image_path)
        plt.figure()
        plt.imshow(img)
        plt.title(filename)
        plt.show()

for filename in os.listdir(img_folder_bad): 
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        image_path = os.path.join(img_folder_bad, filename) 
        img = mpimg.imread(image_path)
        plt.figure()
        plt.imshow(img)
        plt.title(filename)
        plt.show()
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  
)
train_generator = datagen.flow_from_directory(
    '/content/Untitled Folder',
    target_size=(150, 150),
    batch_size=3,  # Smaller batch size due to limited data
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    '/content/Untitled Folder',
    target_size=(150, 150),
    batch_size=2,
    class_mode='binary',
    subset='validation'
)
model=models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])
history=model.fit(
    train_generator,
    steps_per_epoch=4,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=2
)
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.figure()
plt.plot(epochs, acc, 'bo', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
# Plot loss
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
