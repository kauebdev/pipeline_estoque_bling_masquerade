import pandas as pd
from typing import Type

def ReadArchive(path: Type[str], skip: Type[int]):
    return pd.read_excel(path, skiprows=skip)

def ConvertXml_toExcel(path: Type[str]):
    # converter para DataFrame, extraindo apenas os campos úteis 
    return f"{path}.xml"