import pandas as pd


def read_csv_transactions(file_path: str) -> list[dict]:
    df = pd.read_csv(file_path, sep=";")
    df = df.fillna("")
    return df.to_dict(orient="records")

def read_xlsx(file_path: str) -> list[dict]:
    df = pd.read_excel(file_path, engine="openpyxl")
    df = df.fillna("")
    return df.to_dict(orient="records")


read_csv = read_csv_transactions("../transactions.csv")
read_excel = read_xlsx("../transactions_excel.xlsx")
