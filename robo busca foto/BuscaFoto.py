import os
import shutil
import pandas as pd

def copiar_imagens(arquivo_excel, pasta_origem, pasta_destino):
    # Carregar a planilha
    df = pd.read_excel(arquivo_excel)

    # Garantir que a pasta de destino existe
    os.makedirs(pasta_destino, exist_ok=True)

    # Lista para armazenar nomes não encontrados
    nao_encontrados = []

    # Percorrer os nomes das imagens na coluna A
    for nome_imagem in df.iloc[:, 0].dropna():
        nome_imagem_str = str(nome_imagem).strip()
        caminho_origem = os.path.join(pasta_origem, nome_imagem_str)
        caminho_destino = os.path.join(pasta_destino, nome_imagem_str)

        # Verificar se a imagem existe antes de copiar
        if os.path.isfile(caminho_origem):
            shutil.copy2(caminho_origem, caminho_destino)
            print(f'Copiado: {nome_imagem_str}')
        else:
            print(f'Não encontrado: {nome_imagem_str}')
            nao_encontrados.append(nome_imagem_str)

    # Criar arquivo .txt com nomes não encontrados
    if nao_encontrados:
        caminho_txt = os.path.join(os.path.dirname(arquivo_excel), 'nao_encontrados.txt')
        with open(caminho_txt, 'w', encoding='utf-8') as f:
            for item in nao_encontrados:
                f.write(item + '\n')
        print(f'\nArquivo de não encontrados criado: {caminho_txt}')
    else:
        print('\nTodas as imagens foram encontradas.')

# Exemplo de uso
arquivo_excel = r"C:\Users\User\Desktop\robo busca foto\procurar_fotos.xlsx"
pasta_origem = r"C:\Users\User\Desktop\bkp2.0 com risco"
pasta_destino = r"C:\Users\User\Desktop\robo busca foto\fotos"

copiar_imagens(arquivo_excel, pasta_origem, pasta_destino)
