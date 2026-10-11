import pandas as pd

"""
ФУНКЦИЯ ЧТЕНИЯ CSV ФАЙЛОВ С ЗАЩИТОЙ AMOUNT = "NAN"
"""


def read_csv_transactions(file_path: str) -> list[dict]:
    df = pd.read_csv(file_path, sep=";")
    df = df.fillna("")
    return df.to_dict(orient="records")


"""
ФУНКЦИЯ ЧТЕНИЯ XLSX ФАЙЛОВ С ЗАЩИТОЙ AMOUNT = "NAN"
"""


def read_xlsx_transactions(file_path: str) -> list[dict]:
    df = pd.read_excel(file_path, engine="openpyxl")
    df = df.fillna("")
    return df.to_dict(orient="records")
