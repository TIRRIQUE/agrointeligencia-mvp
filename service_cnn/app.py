
from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/log/leaf_image', methods=['POST'])
def log_leaf_image():
    data = request.get_json()

    image_b64 = data.get("imagem")
    label = data.get("rotulo")

    if label not in ["saudavel", "doente"]:
        return jsonify({"erro": "rótulo deve ser 'saudavel' ou 'doente'"}), 400

    try:
        image_data = base64.b64decode(image_b64)
    except:
        return jsonify({"erro": "imagem em Base64 inválida"}), 400

    label_path = os.path.join(UPLOAD_FOLDER, label)
    os.makedirs(label_path, exist_ok=True)

    filename = f"imagem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = os.path.join(label_path, filename)

    with open(file_path, "wb") as f:
        f.write(image_data)

    return jsonify({"mensagem": f"Imagem salva em {file_path}"}), 200

MODEL_PATH = "models/cnn_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/predict/leaf_image', methods=['POST'])
def predict_leaf_image():
    data = request.get_json()
    try:
        img_b64 = data['imagem']
        img_data = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_data)).resize((64,64))
        img_array = np.array(img)/255.0
        if img_array.shape[-1] == 4:  # remover canal alpha, se existir
            img_array = img_array[:,:,:3]
        img_array = np.expand_dims(img_array, axis=0)
        pred = model.predict(img_array)[0][0]
        rotulo = "doente" if pred > 0.5 else "saudavel"
        return {"predicao": rotulo}
    except Exception as e:
        return {"erro": str(e)}, 400

if __name__ == '__main__':
    app.run(port=5002, debug=True)