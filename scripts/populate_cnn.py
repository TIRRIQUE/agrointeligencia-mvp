import requests
import base64
import os

URL = "http://127.0.0.1:5002/log/leaf_image"

BASE_DIR = r"C:\Users\carlo\agrointeligencia-mvp"
local_image_path = os.path.join(BASE_DIR, "sample_images")

folders = ["saudavel", "doente"]

for label in folders:
    folder_path = os.path.join(local_image_path, label)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"[INFO] Pasta criada: {folder_path}")
        continue  # pula, pois não há imagens ainda

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, file_name)

            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

            data = {
                "imagem": img_b64,
                "rotulo": label
            }

            try:
                response = requests.post(URL, json=data)
                print(f"[OK] Enviado: {file_name} -> {response.status_code}")
                print(response.json())
            except Exception as e:
                print(f"[ERRO] Falha ao enviar {file_name}: {e}")
