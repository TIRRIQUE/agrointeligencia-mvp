import pandas as pd
import os


os.makedirs("../data", exist_ok=True)


data = [
    {"note": "Infestação detectada, ação imediata!", "label": "urgente"},
    {"note": "Irrigação concluída sem problemas.", "label": "rotina"},
    {"note": "Doença detectada em algumas folhas.", "label": "urgente"},
    {"note": "Aplicação de adubo realizada.", "label": "rotina"},
    {"note": "Pragas detectadas no talhão leste.", "label": "urgente"},
    {"note": "Monitoramento da irrigação concluído.", "label": "rotina"},
    {"note": "Folhas amareladas, verificar causas.", "label": "urgente"},
    {"note": "Recolhimento de amostras realizado.", "label": "rotina"},
    {"note": "Insetos nocivos observados, tratar imediatamente.", "label": "urgente"},
    {"note": "Rotina de manutenção do equipamento feita.", "label": "rotina"}
]

data = data * 4

df = pd.DataFrame(data)
df.to_csv("../data/field_notes_database.csv", index=False)
print("CSV de teste criado em ../data/field_notes_database.csv")