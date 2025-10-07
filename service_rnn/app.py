
from flask import Flask, request, jsonify
import pandas as pd
import os
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

DATA_PATH = "../data/field_notes_database.csv"
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

@app.route('/log/note', methods=['POST'])
def log_note():
    data = request.get_json()

    if not all(k in data for k in ['texto', 'rotulo']):
        return jsonify({"erro": "Esperado campos: texto e rotulo"}), 400

    if data['rotulo'] not in ['urgente', 'rotina']:
        return jsonify({"erro": "rotulo deve ser 'urgente' ou 'rotina'"}), 400

    df = pd.DataFrame([data])
    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

    return jsonify({"mensagem": "Nota registrada com sucesso!"}), 200

MODEL_PATH = "models/rnn_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"

model = tf.keras.models.load_model(MODEL_PATH)
tokenizer = joblib.load(TOKENIZER_PATH)

@app.route('/predict/note', methods=['POST'])
def predict_note():
    data = request.get_json()
    try:
        texto = data['texto']
        seq = tokenizer.texts_to_sequences([texto])
        padded = pad_sequences(seq, maxlen=20, padding='post')
        pred = model.predict(padded)[0][0]
        rotulo = "urgente" if pred > 0.5 else "rotina"
        return {"predicao": rotulo}
    except Exception as e:
        return {"erro": str(e)}, 400


if __name__ == '__main__':
    app.run(port=5003, debug=True)