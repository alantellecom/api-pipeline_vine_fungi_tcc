
import numpy as np
import tensorflow as tf
from tensorflow import keras

def preprocess_image(image_path,size):
    img = keras.preprocessing.image.load_img(image_path, target_size=(size, size))
    img = keras.preprocessing.image.img_to_array(img)
    img = img/255.
    img = np.expand_dims(img, axis=0)
    return tf.convert_to_tensor(img)

