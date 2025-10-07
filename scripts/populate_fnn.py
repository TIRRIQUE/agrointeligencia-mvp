import os
import requests
import random

BASE_DIR = r"C:\Users\carlo\agrointeligencia-mvp"

SAUDAVEL_DIR = os.path.join(BASE_DIR, "sample_images", "saudavel")
DOENTE_DIR = os.path.join(BASE_DIR, "sample_images", "doente")

URL = "http://127.0.0.1:5001/log/soil_data"

for folder in [SAUDAVEL_DIR, DOENTE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        print(f"[AVISO] Pasta criada: {folder} (adicione imagens nela)")

for i in range(30):
    temperatura = round(random.uniform(20, 35), 1)
    umidade = round(random.uniform(40, 90), 1)
    chuva = round(random.uniform(0, 200), 1)
    ph = round(random.uniform(5.5, 7.5), 1)
    rendimento_alto = 1 if chuva > 100 else 0

    data = {
        "temperatura": temperatura,
        "umidade": umidade,
        "chuva": chuva,
        "ph": ph,
        "rendimento_alto": rendimento_alto
    }

    try:
        response = requests.post(URL, json=data)
        print(f"[{i+1}/30] Enviado -> {data} | Resposta: {response.json()}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar dados: {e}")

if os.listdir(SAUDAVEL_DIR):
    print(f"\nImagens saudáveis encontradas: {len(os.listdir(SAUDAVEL_DIR))}")
else:
    print(f"\n[AVISO] Nenhuma imagem encontrada em {SAUDAVEL_DIR}")
