
import requests
import random

URL = "http://127.0.0.1:5001/log/soil_data"

for i in range(30):  
    temperatura = round(random.uniform(20, 35), 1)
    umidade = round(random.uniform(40, 90), 1)
    chuva = round(random.uniform(0, 200), 1)
    ph = round(random.uniform(5.5, 7.5), 1)
    rendimento_alto = 1 if chuva > 100 else 0  # regra simples

    data = {
        "temperatura": temperatura,
        "umidade": umidade,
        "chuva": chuva,
        "ph": ph,
        "rendimento_alto": rendimento_alto
    }

    response = requests.post(URL, json=data)
    print(response.json())