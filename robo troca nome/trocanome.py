import os
import shutil
import pandas as pd

# Definir os caminhos
pasta_base = "alterar"
pasta_origem = os.path.join(pasta_base, "editar")
pasta_destino = os.path.join(pasta_base, "pronto")
arquivo_excel = os.path.join(pasta_base, "produtos.xlsx")
arquivo_log = os.path.join(pasta_base, "nao_encontrados.txt")

# Criar a pasta de destino caso não exista
os.makedirs(pasta_destino, exist_ok=True)

# Carregar a planilha
try:
    df = pd.read_excel(arquivo_excel, dtype=str)  # Lê todas as colunas como string
except Exception as e:
    print(f"Erro ao abrir a planilha: {e}")
    exit()

# Inicializar contadores e lista de erros
copiados = 0
nao_encontrados = 0
lista_nao_encontrados = []

# Renomear e copiar os arquivos
for index, row in df.iterrows():
    nome_antigo = row.iloc[0]  # A primeira coluna (Coluna A) contém o nome original

    if pd.isna(nome_antigo):
        continue  # Ignora linhas onde o nome original está vazio

    for nome_novo in row.iloc[1:]:  # Percorre todas as colunas a partir da segunda (Coluna B em diante)
        if pd.isna(nome_novo):
            continue  # Ignora células vazias

        caminho_origem = os.path.join(pasta_origem, f"{nome_antigo}.png")
        caminho_destino = os.path.join(pasta_destino, f"{nome_novo}.png")

        if os.path.exists(caminho_origem):
            shutil.copy2(caminho_origem, caminho_destino)
            copiados += 1
            print(f"Copiado: {caminho_origem} -> {caminho_destino}")
        else:
            nao_encontrados += 1
            lista_nao_encontrados.append(caminho_origem)
            print(f"Arquivo não encontrado: {caminho_origem}")

# Salvar log de arquivos não encontrados
if lista_nao_encontrados:
    with open(arquivo_log, 'w', encoding='utf-8') as f:
        for item in lista_nao_encontrados:
            f.write(item + '\n')
    print(f"\nLista de arquivos não encontrados salva em: {arquivo_log}")

# Resumo do processo
print("\nResumo do processo:")
print(f"Total de arquivos copiados: {copiados}")
print(f"Total de arquivos não encontrados: {nao_encontrados}")
