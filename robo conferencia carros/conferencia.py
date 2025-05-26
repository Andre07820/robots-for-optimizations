import pandas as pd
import re

# Carregar a planilha
file_path = "C:/Users/User/Desktop/robo conferencia carros/carros a conferir.xlsx"
df = pd.read_excel(file_path)


df = pd.read_excel(file_path, dtype={"nomefoto": str})

# Ajuste os nomes das colunas
coluna_A = "veiculo"
coluna_B = "ano inicial"  # Atenção ao espaço no final
coluna_C = "ano final"
coluna_D = "nomefoto"
coluna_E = "CARRO + ANO INICIAL"
coluna_F = "carro correspondente"
coluna_G = "OK / F"
coluna_H = "Carros+ano"

# Criar uma lista formatada dos carros existentes
carros_existentes = df[coluna_H].dropna().astype(str).str.strip().str.lower().tolist()

# Função para verificar se o carro existe dentro do intervalo de anos
def verificar_carro(linha):
    nome_carro = str(linha[coluna_A]).strip().lower()
    
    # Obter ano inicial e final, lidando com NaN
    ano_inicial = linha[coluna_B]
    ano_final = linha[coluna_C]

    if pd.isna(ano_inicial):  # Se o ano inicial estiver vazio, ignorar linha
        return ("carro não existe", "F")
    
    ano_inicial = int(ano_inicial)  # Converter ano inicial para inteiro
    
    if pd.isna(ano_final):  
        ano_final = ano_inicial  # Se ano final for NaN, assumir que é igual ao inicial
    else:
        ano_final = int(ano_final)  # Converter ano final para inteiro

    for carro_disponivel in carros_existentes:
        match = re.match(r"(.+?)\s(\d{4})$", carro_disponivel)  # Separar nome e ano
        if match:
            nome_disponivel, ano_disponivel = match.groups()
            ano_disponivel = int(ano_disponivel)

            # Se for o mesmo carro e o ano estiver no intervalo, retorna
            if nome_carro == nome_disponivel and ano_inicial <= ano_disponivel <= ano_final:
                return (f"{nome_carro} {ano_disponivel}", "OK")

    return ("carro não existe", "F")

# Aplicar a função para preencher a coluna F e G
df[[coluna_F, coluna_G]] = df.apply(verificar_carro, axis=1).apply(pd.Series)

# Segunda verificação: garantir que todas as repetições de um mesmo código na coluna D tenham o mesmo status
# Se alguma linha do mesmo código estiver com "F", todas as ocorrências desse código devem ser "F"
status_por_codigo = df.groupby(coluna_D)[coluna_G].transform(lambda x: "F" if "F" in x.values else "OK")
df[coluna_G] = status_por_codigo

# Salvar a planilha modificada
output_path = "C:/Users/User/Desktop/robo conferencia carros/Planilha_Atualizada.xlsx"
df.to_excel(output_path, index=False)

print(f"✅ Planilha processada com sucesso! Arquivo salvo em: {output_path}")
