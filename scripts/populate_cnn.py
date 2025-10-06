import requests
import base64
import os

URL = "http://127.0.0.1:5002/log/leaf_image"

folders = ["saudavel", "doente"]


local_image_path = os.path.join("..", "sample_images")  

for label in folders:
    folder_path = os.path.join(local_image_path, label)
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            with open(os.path.join(folder_path, file_name), "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

            data = {
                "imagem": img_b64,
                "rotulo": label
            }
            response = requests.post(URL, json=data)
            print(response.json())