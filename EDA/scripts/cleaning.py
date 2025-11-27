import pandas as pd
import numpy as np

def clean_duplicated(df):
    df_copy = df.copy()
    print(f'Número de filas duplicadas sin tener en cuenta la primera ocurrencia: {df_copy.duplicated().sum()}')
    df_copy.drop_duplicates(keep='first', inplace=True)
    return df_copy
