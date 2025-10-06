
from PIL import Image
import os


os.makedirs("sample_images/saudavel", exist_ok=True)
os.makedirs("sample_images/doente", exist_ok=True)


for i in range(5):
    
    Image.new('RGB', (100, 100), color='white').save(f'sample_images/saudavel/img{i}.jpg')
    
    Image.new('RGB', (100, 100), color='black').save(f'sample_images/doente/img{i}.jpg')

print("Pastas e imagens de teste criadas com sucesso!")