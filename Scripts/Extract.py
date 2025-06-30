import pandas as pd
import os
import sys
import requests
import json
import time
from typing import Type

def ReadArchive(path: Type[str], skip: Type[int]):
    return pd.read_excel(path, skiprows=skip)

def ConvertXml_toExcel(path: Type[str]):
    # converter para DataFrame, extraindo apenas os campos úteis 
    return f"{path}.xml"

def GetToken(): # rodar o tokenGetter_withFlask_bling\src\rodar_server.py para gerar o token
    tokens_file = r"D:\kaue\projetos\tokenGetter_withFlask_bling\Data\tokens.json" # caminho do arquivo JSON com os tokens
    # abre o tokens_file "R" le ele e salva como file
    with open(tokens_file, "r") as file:
        tokens = json.load(file) 
        token = tokens[len(tokens)-1]["access_token"] # pega o último token
        return token

def GetProdutos(token: Type[str]):
    URL = f"https://api.bling.com.br/Api/v3/produtos" # url com endpoint de produtos
    page = 1 
    has_page = True # para repetição
    produtos = [] # list que vai ser colocada os produtos
    
    while has_page:
        # enquanto tiver página, vai pegando os produtos
        # se não tiver mais produtos, sai do loop
        params = {
            "criterio": 2,
            "pagina": page
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

        response = requests.get(URL,params=params, headers=headers)
       
        if response.status_code == 200:
            Data = response.json().get('Data', []) # extrai os dados do JSON (BLING RETONAR TUDO NO Data), 
            if not Data:
                has_page = False
            page += 1 # incremneta opara a proxima pagina
            produtos.extend(Data) # adiciona os produtos da página atual à lista de produtos
            time.sleep(0.5) # espera 0.5 segundo para não sobrecarregar a API --
            # 3 requisições por segundo
            # 120.000 requisições por dia
            print(f"Página {page} obtida com sucesso, total de produtos: {len(Data)}")
        else:
            print(f"Erro ao obter produtos: {response.status_code} - {response.text}")
            return None
    print(f"Total de produtos obtidos: {len(produtos)}")
    # converte a lista de produtos em um DataFrame
    produtos = pd.DataFrame(produtos)
    return produtos   

def GetFile(extension):
    
    # obtém o diretório atual do script
    dir = os.path.dirname(os.path.abspath(__file__))

    # constroi o caminho para o diretório 'Data'
    # A partir do diretório atual (onde o script está sendo executado)
    # e sobe um nível para o diretório pai, depois entra na pasta 'Data'
    # Isso é útil para garantir que o caminho seja relativo ao local do script
    # e não ao diretório de trabalho atual do Python.

    # ele entra na pasta data, cirnado o pycache pois o script está dentro de uma pasta diferente da data e acessa ela tenmporariamente
    dir_data_cache = os.path.join(dir, '..', 'Data')
    dir_data_cache = os.path.normpath(dir_data_cache)

    files_found = []
    all_files = os.listdir(dir_data_cache) # epga a lsiat com tdodos os arquivos na pasta data

    for file in all_files: # percorre a lista com todos os arquivos
        full_path = os.path.join(dir_data_cache, file)
        if os.path.isfile(full_path) and file.lower().endswith(extension.lower()): #  for um arquivo e terminar com a extensão
             files_found.append(full_path)

    if len(files_found) > 1  : # se tiver mais de um arquivo com a extensão
        print(f"Mais de um arquivo com a extensão {extension} encontrado. Erro: apenas um arquivo é permitido.")
        return None
    
    elif len(files_found) == 0: # se não tiver nenhum arquivo com a extensão
        print(f"Nenhum arquivo com a extensão {extension} encontrado.")
        return None
    
    # se tiver apenas um arquivo com a extensão
    print(f"Arquivo encontrado: {files_found[0]}")
    return files_found[0]

        