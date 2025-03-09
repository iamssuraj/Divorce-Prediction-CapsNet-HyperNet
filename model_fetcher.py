import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from imblearn.over_sampling  import SMOTE
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from tensorflow.keras import layers, models, regularizers
import os
print("📂 Current Directory:", os.getcwd())
print("📁 Files in Directory:", os.listdir(os.getcwd()))

# Define your capsule layer
class CapsuleLayer(layers.Layer):
    def __init__(self, num_capsules, capsule_dim, routings=3, kernel_initializer='glorot_uniform', **kwargs):
        super(CapsuleLayer, self).__init__(**kwargs)
        self.num_capsules = num_capsules
        self.capsule_dim = capsule_dim
        self.routings = routings
        self.kernel_initializer = keras.initializers.get(kernel_initializer)

    def build(self, input_shape):
        input_dim = input_shape[-1]
        self.kernel = self.add_weight(name='kernel', shape=(input_dim, self.num_capsules * self.capsule_dim),
                                      initializer=self.kernel_initializer, trainable=True)
        super(CapsuleLayer, self).build(input_shape)

    def call(self, u_vecs):
        u_hat_vecs = keras.backend.dot(u_vecs, self.kernel)
        u_hat_vecs = keras.backend.reshape(u_hat_vecs, (-1, self.num_capsules, self.capsule_dim))
        return self.squash(u_hat_vecs)

    def squash(self, vectors):
        epsilon = 1e-6
        squared_norm = keras.backend.sum(keras.backend.square(vectors), axis=-1, keepdims=True)
        scale = squared_norm / (1 + squared_norm) / keras.backend.sqrt(squared_norm + epsilon)
        return scale * vectors

    def compute_output_shape(self, input_shape):
        return tuple([None, self.num_capsules, self.capsule_dim])

# Build the Hypernetwork model
def build_hypernetwork(input_shape, num_classes):
    x = layers.Input(shape=input_shape)
    hyper_output = layers.Dense(22, activation='relu')(x)  # Adjust the number of neurons as needed
    return models.Model(inputs=x, outputs=hyper_output)

# Build the Capsule Neural Network model
def build_capsule_model(input_shape, num_classes):
    x = layers.Input(shape=input_shape)
    capsule = CapsuleLayer(num_capsules=100, capsule_dim=100, routings=7)(x)
    output = layers.Flatten()(capsule)
    output = layers.Dropout(0.5)(output)  # Dropout layer added
    output = layers.Dense(num_classes, activation='sigmoid', kernel_regularizer=regularizers.l2(0.01))(output)  # L2 regularization added
    return models.Model(inputs=x, outputs=output)

input_shape = (22,)
num_classes = 2

hypernetwork = build_hypernetwork(input_shape, num_classes)
capsule_model = build_capsule_model(input_shape, num_classes)

combined_model = keras.Sequential([hypernetwork, capsule_model])

custom_objects = {'CapsuleLayer': CapsuleLayer}
combined_model = load_model('Divorce-Prediction-CapsNet-HyperNet/my_model.h5', custom_objects=custom_objects)
combined_model.save("Divorce-Prediction-CapsNet-HyperNet/my_model.h5")

weights = combined_model.get_weights()
# print(weights)