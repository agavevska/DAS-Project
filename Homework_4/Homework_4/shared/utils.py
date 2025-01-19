import pandas as pd


def validate_csv(file_path):
    try:
        pd.read_csv(file_path)
        return True
    except Exception as e:
        return False, str(e)
