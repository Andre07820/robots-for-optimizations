import cv2
import os

def resize_images_in_folder(input_folder, output_folder, target_size=(1000,1000)):
    # Criar a pasta de saída, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todos os arquivos na pasta
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Filtrar imagens válidas
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Carregar a imagem
            image = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if image is None:
                print(f"Erro ao carregar {filename}. Pulando...")
                continue

            # Obter tamanho original da imagem
            h, w = image.shape[:2]

            # Calcular o fator de escala mantendo a proporção
            scale = min(target_size[0] / w, target_size[1] / h)
            new_size = (int(w * scale), int(h * scale))

            # Redimensionar a imagem
            resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)

            # Salvar imagem redimensionada
            cv2.imwrite(output_path, resized_image)
            print(f"Imagem {filename} redimensionada de {w}x{h} para {new_size[0]}x{new_size[1]}")

# Caminhos das pastas
input_folder = r"C:\Users\User\Desktop\robo tamanho qualidade\imagens_originais"
output_folder = r"C:\Users\User\Desktop\robo tamanho qualidade\imagens_redimensionadas"

# Rodar o script
resize_images_in_folder(input_folder, output_folder)
