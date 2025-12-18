import pandas as pd
import os

# Substitua 'seu_arquivo.xls' pelo caminho/nome real do seu arquivo
caminho_do_arquivo = '_NotaCor_05122025_814336.xls'

# try:
# O pandas detectará automaticamente o formato .xls e usará o engine 'xlrd'
df = pd.read_excel(caminho_do_arquivo, engine='xlrd')

# Exibe as primeiras 5 linhas do DataFrame
print(df)

# except FileNotFoundError as e.:
#     print(e)
# except Exception as e:
#     print(f"Ocorreu um erro ao ler o arquivo: {e}")