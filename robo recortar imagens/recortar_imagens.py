from PIL import Image
import numpy as np
import os

# Caminhos das pastas
pasta_origem = "C:/Users/User/Desktop/robo recortar imagens/editar"
pasta_destino = "C:/Users/User/Desktop/robo recortar imagens/pronto"

# Certifique-se de que a pasta de destino exista
os.makedirs(pasta_destino, exist_ok=True)

# Loop pelas imagens da pasta de origem
for nome_arquivo in os.listdir(pasta_origem):
    if nome_arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        caminho_imagem = os.path.join(pasta_origem, nome_arquivo)
        
        try:
            img = Image.open(caminho_imagem).convert("RGB")
            img_np = np.array(img)

            # Encontrar os pixels que não são brancos
            non_white_pixels = np.where(np.any(img_np != [255, 255, 255], axis=-1))

            if non_white_pixels[0].size > 0 and non_white_pixels[1].size > 0:
                top, bottom = non_white_pixels[0].min(), non_white_pixels[0].max()
                left, right = non_white_pixels[1].min(), non_white_pixels[1].max()

                # Recortar a imagem
                cropped_img = img.crop((left, top, right + 1, bottom + 1))

                # Salvar no destino
                caminho_saida = os.path.join(pasta_destino, nome_arquivo)
                cropped_img.save(caminho_saida)
                print(f"Recortada: {nome_arquivo}")
            else:
                print(f"Imagem em branco: {nome_arquivo}")
        
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")
