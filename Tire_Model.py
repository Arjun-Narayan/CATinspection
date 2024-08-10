
import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'tire-texture-image-recognition:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1731575%2F2830785%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240810%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240810T171846Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D8c8a827dcbab0d92c010a408f7e21a82352eb35c41da9477e67fc7f2a62bbed668b1befcecaf7489f861e795e4f0560a9020e77fb54350ed73e4fa24eff0577c2937a78448daa609cdf9b343f9c9b7f1019d4a281c6cadb90bfe773fcfe9a4b46270d8b88c9921a8ea1b685fa7f4f21fa14f5c3dd4a5d8cff71b61dc60d1422b2ae36dda94ec8eb156e054c693eecdac498d2754f277bc125f26ef423a86abfab2a05a46fab4b4a0f7f2696dfd7e76c0ca5d5c6962974131ae2990d33c3598d901d5d88bb6a0fc36c3a19da89e3f40c0301d2de7743faa39cc392b73b9945b26c55d8aa495597eef4c042ac1e17451cc4e93a9dde4f4393123e7146927fc42c3'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""# **INCLUDE LIBRARY**

import several necessary libraries to work with the data before doing analysis and modeling
"""

#Analysis
import pandas as pd
import numpy as np

#Visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#NN Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator # Import from tensorflow.keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import * # Import layers from tensorflow.keras
from tensorflow.keras.callbacks import ModelCheckpoint # Import callbacks from tensorflow.keras

#Evaluation
from sklearn.metrics import confusion_matrix, classification_report

"""# **AUGMENTATION**

We apply on-the-fly data augmentation, a technique to expand the training dataset size by creating a modified version of the original image which can improve model performance and the ability to generalize. We will use with the following parameters:

- `rotation_range`: Degree range for random rotations. We choose 360 degrees since the product is a round object.
- `width_shift_range`: Fraction range of the total width to be shifted.
- `height_shift_range`: Fraction range of the total height to be shifted.
- `shear_range`: Degree range for random shear in a counter-clockwise direction.
- `zoom_range`: Fraction range for random zoom.
- `horizontal_flip` and `vertical_flip` are set to True for randomly flip image horizontally and vertically.
- `brightness_range`: Fraction range for picking a brightness shift value.

Other parameters:

- `rescale`: Eescale the pixel values to be in range 0 and 1.
- `validation_split`: Reserve 20% of the training data for validation, and the rest 80% for model fitting.
"""

train_generator = ImageDataGenerator(rotation_range = 360,
                                     width_shift_range = 0.05,
                                     height_shift_range = 0.05,
                                     shear_range = 0.05,
                                     zoom_range = 0.05,
                                     horizontal_flip = True,
                                     vertical_flip = True,
                                     brightness_range = [0.75, 1.25],
                                     rescale = 1./255,
                                     validation_split = 0.2)
IMAGE_DIR = "../input/tire-texture-image-recognition/Tire Textures/"

IMAGE_SIZE = (379, 379)
BATCH_SIZE = 64
SEED_NUMBER = 123

gen_args = dict(target_size = IMAGE_SIZE,
                color_mode = "grayscale",
                batch_size = BATCH_SIZE,
                class_mode = "binary",
                classes = {"normal": 0, "cracked": 1},
                seed = SEED_NUMBER)

train_dataset = train_generator.flow_from_directory(
                                        directory = IMAGE_DIR + "training_data",
                                        subset = "training", shuffle = True, **gen_args)
validation_dataset = train_generator.flow_from_directory(
                                        directory = IMAGE_DIR + "training_data",
                                        subset = "validation", shuffle = True, **gen_args)

test_generator = ImageDataGenerator(rescale = 1./255)
test_dataset = test_generator.flow_from_directory(directory = IMAGE_DIR + "testing_data",
                                                  shuffle = False,
                                                  **gen_args)
mapping_class = {0: "normal", 1: "cracked"}
mapping_class

def visualizeImageBatch(dataset, title):
    images, labels = next(iter(dataset))
    images = images.reshape(BATCH_SIZE, *IMAGE_SIZE)
    fig, axes = plt.subplots(8, 8, figsize=(16,16))

    for ax, img, label in zip(axes.flat, images, labels):
        ax.imshow(img, cmap = "gray")
        ax.axis("off")
        ax.set_title(mapping_class[label], size = 20)

    plt.tight_layout()
    fig.suptitle(title, size = 30, y = 1.05, fontweight = "bold")
    plt.show()

    return images

train_images = visualizeImageBatch(train_dataset,
                                   "FIRST BATCH OF THE TRAINING IMAGES\n(WITH DATA AUGMENTATION)")

test_images = visualizeImageBatch(test_dataset,
                                  "FIRST BATCH OF THE TEST IMAGES\n(WITHOUT DATA AUGMENTATION)")
model_cnn = Sequential(
    [
        # First convolutional layer
        Conv2D(filters = 128,
               kernel_size = 3,
               strides = 2,
               activation = "relu",
               input_shape = IMAGE_SIZE + (1, )),

        # First pooling layer
        MaxPooling2D(pool_size = 2,
                     strides = 2),

        # Second convolutional layer
        Conv2D(filters = 64,
               kernel_size = 3,
               strides = 2,
               activation = "relu"),

        # Second pooling layer
        MaxPooling2D(pool_size = 2,
                     strides = 2),

        # Third convolutional layer
        Conv2D(filters = 32,
               kernel_size = 3,
               strides = 2,
               activation = "relu"),

        # Third pooling layer
        MaxPooling2D(pool_size = 2,
                     strides = 2),

        # Forth convolutional layer
        Conv2D(filters = 16,
               kernel_size = 3,
               strides = 2,
               activation = "relu"),

        # Forth pooling layer
        MaxPooling2D(pool_size = 2,
                     strides = 2),

        # Flattening
        Flatten(),

        # Fully-connected layer
        Dense(128, activation = "relu"),
        Dropout(rate = 0.2),

        Dense(64, activation = "relu"),
        Dropout(rate = 0.2),

        Dense(1, activation = "sigmoid")
    ]
)

model_cnn.summary()

"""### Compile the Model

Next, we specify how the model backpropagates or update the weights after each batch feed-forward. We use `adam` optimizer and a loss function `binary cross-entropy` since we are dealing with binary classification problem. The metrics used to monitor the training progress is accuracy.
"""

model_cnn.compile(optimizer = 'adam',
              loss = 'binary_crossentropy',
              metrics = ['accuracy'])

"""## Model Fitting
Before we do model fitting, let's check whether GPU is available or not.
"""

checkpoint = ModelCheckpoint('model/cnn_tire_texture_model.keras', # Change the file extension to '.keras'
                             verbose = 1,
                             save_best_only = True,
                             monitor='val_loss',
                             mode='min')

model_cnn.fit(train_dataset,
                    validation_data = validation_dataset,
                    batch_size = 16,
                    epochs = 20,
                    callbacks = [checkpoint],
                    verbose = 1)

plt.subplots(figsize = (8, 6))
sns.lineplot(data = pd.DataFrame(model_cnn.history.history,
                                 index = range(1, 1+len(model_cnn.history.epoch))))
plt.title("TRAINING EVALUATION", fontweight = "bold", fontsize = 20)
plt.xlabel("Epochs")
plt.ylabel("Metrics")

plt.legend(labels = ['val loss', 'val accuracy', 'train loss', 'train accuracy'])
plt.show()
model_cnn.save('CNN Tire Texture Classification.h5')

from google.colab import files # Import the necessary module
files.download('CNN Tire Texture Classification.h5')

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

best_model = load_model("model/cnn_tire_texture_model.hdf5")

y_pred_prob = best_model.predict(test_dataset)
THRESHOLD = 0.5
y_pred_class = (y_pred_prob >= THRESHOLD).reshape(-1,)
y_true_class = test_dataset.classes[test_dataset.index_array]

pd.DataFrame(
    confusion_matrix(y_true_class, y_pred_class),
    index = [["Actual", "Actual"], ["normal", "cracked"]],
    columns = [["Predicted", "Predicted"], ["normal", "cracked"]],
)
print(classification_report(y_true_class, y_pred_class, digits = 4))