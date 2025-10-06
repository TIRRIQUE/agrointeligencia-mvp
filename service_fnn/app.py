
from flask import Flask, request, jsonify
import pandas as pd
import os
import joblib
import numpy as np

app = Flask(__name__)
DATA_PATH = "../data/soil_database.csv"

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

@app.route('/log/soil_data', methods=['POST'])
def log_soil_data():
    data = request.get_json()

    expected_keys = ['temperatura', 'umidade', 'chuva', 'ph', 'rendimento_alto']
    if not all(k in data for k in expected_keys):
        return jsonify({"erro": f"Esperado campos: {expected_keys}"}), 400

    df = pd.DataFrame([data])
    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

    return jsonify({"mensagem": "Dados de solo registrados com sucesso!"}), 200

MODEL_PATH = "models/fnn_model.pkl"
SCALER_PATH = "models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.route('/predict/soil_data', methods=['POST'])
def predict_soil_data():
    data = request.get_json()
    try:
        X = np.array([[data['temperatura'], data['umidade'], data['chuva'], data['ph']]])
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]
        return {"predicao_rendimento_alto": int(pred)}
    except Exception as e:
        return {"erro": str(e)}, 400


if __name__ == '__main__':
    app.run(port=5001, debug=True)