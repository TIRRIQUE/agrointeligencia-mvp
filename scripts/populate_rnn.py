# scripts/populate_rnn.py
import requests
import time

URL = "http://127.0.0.1:5003/log/note"

notas_urgente = [
    "Infestação severa de ferrugem asiática detectada no talhão norte.",
    "Praga detectada no milho, ação imediata necessária.",
    "Doença rápida se espalhando nas folhas do feijão, inspecionar imediatamente."
]

notas_rotina = [
    "Irrigação do setor sul concluída conforme cronograma.",
    "Colheita do trigo está dentro do planejado, sem anomalias.",
    "Verificação de solo realizada, ph e umidade dentro do esperado."
]

# Garante 20 notas de cada tipo
notas_urgente = (notas_urgente * 7)[:20]
notas_rotina = (notas_rotina * 7)[:20]

def enviar_nota(texto, rotulo):
    data = {"texto": texto, "rotulo": rotulo}
    try:
        response = requests.post(URL, json=data, timeout=5)
        print(response.json())
    except requests.exceptions.ConnectionError:
        print(f"[ERRO] Não foi possível conectar ao servidor em {URL}. Certifique-se de que ele está rodando.")
    except requests.exceptions.Timeout:
        print(f"[ERRO] Timeout ao enviar nota: {texto}")

for texto in notas_urgente:
    enviar_nota(texto, "urgente")
    time.sleep(0.1)  

for texto in notas_rotina:
    enviar_nota(texto, "rotina")
    time.sleep(0.1)