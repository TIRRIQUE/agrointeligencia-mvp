import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib
import os


DATA_PATH = "../data/soil_database.csv"
MODEL_PATH = "models/fnn_model.pkl"
SCALER_PATH = "models/scaler.pkl"


os.makedirs("models", exist_ok=True)


df = pd.read_csv(DATA_PATH)
X = df[['temperatura', 'umidade', 'chuva', 'ph']]
y = df['rendimento_alto']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = MLPClassifier(hidden_layer_sizes=(16,16), max_iter=500, random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("Modelo FNN treinado e salvo com sucesso!")