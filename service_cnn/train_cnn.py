
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

DATA_DIR = "../sample_images"
MODEL_PATH = "models/cnn_model.h5"

os.makedirs("models", exist_ok=True)

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