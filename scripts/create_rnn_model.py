import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
import os


MODEL_PATH = "../service_rnn/models/rnn_model.h5"
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

model = Sequential([
    Embedding(input_dim=1000, output_dim=64),
    SimpleRNN(32),
    Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.save(MODEL_PATH)
print(f"Modelo salvo em {MODEL_PATH}")