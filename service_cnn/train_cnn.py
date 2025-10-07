import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np

BASE_DIR = r"C:\Users\carlo\agrointeligencia-mvp"
DATA_DIR = os.path.join(BASE_DIR, "sample_images")
MODEL_PATH = os.path.join(BASE_DIR, "models", "cnn_model.h5")

SAUDAVEL_DIR = os.path.join(DATA_DIR, "saudavel")
DOENTE_DIR = os.path.join(DATA_DIR, "doente")
os.makedirs(SAUDAVEL_DIR, exist_ok=True)
os.makedirs(DOENTE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def gerar_imagens_fake(pasta, cor):
    if not os.listdir(pasta):
        print(f"[INFO] Gerando imagens falsas em: {pasta}")
        for i in range(5):
            img = Image.new("RGB", (64, 64), color=cor)
            img.save(os.path.join(pasta, f"fake_{i}.jpg"))

gerar_imagens_fake(SAUDAVEL_DIR, (0, 255, 0)) 
gerar_imagens_fake(DOENTE_DIR, (255, 0, 0))   

train_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(64, 64),
    batch_size=4,
    class_mode='binary',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(64, 64),
    batch_size=4,
    class_mode='binary',
    subset='validation'
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(64, 64, 3)),
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("\n🧠 Iniciando treinamento da CNN...")
model.fit(train_generator, validation_data=val_generator, epochs=5)

model.save(MODEL_PATH)
print(f"\n✅ Modelo CNN treinado e salvo com sucesso em: {MODEL_PATH}")