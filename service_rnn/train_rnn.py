import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import joblib


DATA_PATH = "../data/field_notes_database.csv"
MODEL_PATH = "models/rnn_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"
os.makedirs("models", exist_ok=True)

df = pd.read_csv(DATA_PATH)

df.columns = df.columns.str.strip()

texts = df['texto'].values
labels = [1 if r=="urgente" else 0 for r in df['rotulo'].values]


tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences, maxlen=20, padding='post')


model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=1000, output_dim=16, input_length=20),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(padded, labels, epochs=5, batch_size=4)


model.save(MODEL_PATH)
joblib.dump(tokenizer, TOKENIZER_PATH)

print("Modelo RNN treinado e salvo com sucesso!")