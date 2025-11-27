import pandas as pd
import numpy as np

def clean_duplicated_thresh_nulls(df):
    '''
    Función que limpia el DF original de duplicados, manteniendo la primera ocurrencia, y eliminación de filas con más de 9 nulos entre sus valores.
    Además, imprime una serie de información para tener en cuenta cuántas filas se han eliminado.

    Arg:
    df (pd.Dataframe): DF sobre el que se quiere hacer la limpieza.

    Returns:
    pd.DataFrame: DF limpio
    '''
    df_copy = df.copy()
    print(f'Número de filas duplicadas sin tener en cuenta la primera ocurrencia: {df_copy.duplicated().sum()}')

    df_copy.drop_duplicates(keep='first', inplace=True)
    len_con_duplicados = len(df)
    len_sin_thresh = len(df_copy)
    print('Número de registros en el DF con duplicados ->', len_con_duplicados)
    print('\nNúmero de registros en el DF sin publicados ->', len_sin_thresh)

    df_copy.dropna(thresh=9, inplace=True)
    len_con_thresh = len(df_copy)
    diff = len_sin_thresh - len_con_thresh
    print('Número de registros en el DF con thresh->', len_con_thresh)
    print('\nDiferencia entre sin thresh y con thresh ->', diff)

    return df_copy
