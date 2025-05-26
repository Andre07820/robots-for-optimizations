import cv2
import os
import numpy as np

def processar_imagem(caminho_entrada, caminho_saida):
    imagem = cv2.imread(caminho_entrada)
    if imagem is None:
        print(f"Erro ao carregar imagem: {caminho_entrada}")
        return

    altura_total, largura = imagem.shape[:2]

    # Define os limites fixos conforme a estrutura da imagem
    parte_pecas = imagem[0:1000, :]
    parte_carros = imagem[1000:altura_total, :]

    # Converter para tons de cinza e aplicar limiar para segmentar as peças
    cinza = cv2.cvtColor(parte_pecas, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cinza, 240, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos para detectar a peça
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        print(f"Nenhuma peça detectada em: {caminho_entrada}")
        return

    # Ordenar contornos pela área (maior primeiro) e pegar o maior
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)

    # Recorta o bounding box da maior peça
    x, y, w, h = cv2.boundingRect(contornos[0])
    peca_cortada = parte_pecas[y:y+h, x:x+w]

    # Criar uma nova imagem branca com tamanho original da parte da peça
    nova_parte_pecas = np.ones_like(parte_pecas) * 255

    # Calcular posição para centralizar a peça na nova imagem
    x_offset = (largura - w) // 2
    y_offset = (1000 - h) // 2
    nova_parte_pecas[y_offset:y_offset + h, x_offset:x_offset + w] = peca_cortada

    # Concatenar com a parte dos carros
    imagem_final = np.vstack((nova_parte_pecas, parte_carros))

    # Salvar imagem final
    nome_arquivo = os.path.basename(caminho_entrada)
    caminho_saida_completo = os.path.join(caminho_saida, nome_arquivo)
    cv2.imwrite(caminho_saida_completo, imagem_final)
    print(f"Imagem processada e salva em: {caminho_saida_completo}")

# Caminhos das pastas
pasta_entrada = r'C:\Users\User\Desktop\robo foto unitaria\kit'
pasta_saida = r'C:\Users\User\Desktop\robo foto unitaria\pronto'

# Criar pasta de saída se não existir
os.makedirs(pasta_saida, exist_ok=True)

# Processar todas as imagens na pasta de entrada
for arquivo in os.listdir(pasta_entrada):
    if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
        caminho_arquivo = os.path.join(pasta_entrada, arquivo)
        processar_imagem(caminho_arquivo, pasta_saida)
