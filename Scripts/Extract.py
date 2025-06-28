import pandas as pd
import os
import requests
import json
from typing import Type

def ReadArchive(path: Type[str], skip: Type[int]):
    return pd.read_excel(path, skiprows=skip)

def ConvertXml_toExcel(path: Type[str]):
    # converter para DataFrame, extraindo apenas os campos úteis 
    return f"{path}.xml"

def GetToken(): # rodar o tokenGetter_withFlask_bling\src\rodar_server.py para gerar o token
    tokens_file = r"D:\kaue\projetos\tokenGetter_withFlask_bling\data\tokens.json" # caminho do arquivo JSON com os tokens
    # abre o tokens_file "R" le ele e salva como file
    with open(tokens_file, "r") as file:
        tokens = json.load(file) 
        token = tokens[len(tokens)-1]["access_token"] # pega o último token
        return token

def GetProdutos(token: Type[str]):
    endpoint = "produtos" 
    url = f"https://api.bling.com.br/Api/v3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter produtos: {response.status_code} - {response.text}")
        return None