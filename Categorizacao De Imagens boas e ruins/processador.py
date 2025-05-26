import os
import cv2
import numpy as np
from skimage.filters import laplace
from skimage import exposure

# Diretórios de entrada e saída
PASTA_IMAGENS = "imagens"
PASTA_BOAS = "boas"
PASTA_RUINS = "ruins"

# Criar pastas de saída se não existirem
os.makedirs(PASTA_BOAS, exist_ok=True)
os.makedirs(PASTA_RUINS, exist_ok=True)

# Extensões de imagens permitidas
EXTENSOES_IMAGENS = {".jpg", ".jpeg", ".png", ".bmp", ".jfif"}

def calcular_nitidez(imagem):
    """ Calcula a nitidez usando Laplacian Variance + Tenengrad. """
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    # Laplacian Variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Tenengrad (Gradiente de Sobel)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    tenengrad = np.mean(sobel_x**2 + sobel_y**2)

    return laplacian_var, tenengrad

def calcular_ruido(imagem):
    """ Mede a quantidade de ruído usando um filtro Canny. """
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return np.mean(edges)

def calcular_contraste(imagem):
    """ Mede o contraste usando a distribuição do histograma. """
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    return exposure.is_low_contrast(gray, fraction_threshold=0.05)

def classificar_imagem(caminho):
    """ Classifica a imagem como boa ou ruim. """
    imagem = cv2.imread(caminho)
    if imagem is None:
        return "ruim"

    # Cálculos de qualidade
    nitidez, tenengrad = calcular_nitidez(imagem)
    ruido = calcular_ruido(imagem)
    baixo_contraste = calcular_contraste(imagem)

    # Ajuste de limiares para imagens boas
    if nitidez > 35 and tenengrad > 1 and ruido < 1000 and not baixo_contraste:
        return "boa"
    else:
        return "ruim"

def processar_imagens():
    """ Processa todas as imagens e as move para pastas de acordo com a qualidade. """
    for arquivo in os.listdir(PASTA_IMAGENS):
        caminho = os.path.join(PASTA_IMAGENS, arquivo)
        
        # Ignorar arquivos ocultos e não imagens
        if not os.path.isfile(caminho) or not any(arquivo.lower().endswith(ext) for ext in EXTENSOES_IMAGENS):
            continue  

        classificacao = classificar_imagem(caminho)
        
        if classificacao == "boa":
            destino = os.path.join(PASTA_BOAS, arquivo)
        else:
            destino = os.path.join(PASTA_RUINS, arquivo)
        
        # Evitar erro se o arquivo já existir no destino
        if os.path.exists(destino):
            os.remove(destino)  # Deleta a cópia antiga antes de mover
        
        os.rename(caminho, destino)
        print(f"Imagem {arquivo} -> {classificacao}")

# Executar o processamento
processar_imagens()
