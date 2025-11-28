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

    df_copy.dropna(thresh=len(df.columns)/2, inplace=True)
    len_con_thresh = len(df_copy)
    diff = len_sin_thresh - len_con_thresh
    print('Número de registros en el DF con thresh->', len_con_thresh)
    print('\nDiferencia entre sin thresh y con thresh ->', diff)

    return df_copy

def change_to_numeric(df, num_cols):
    '''
    Función que cambia el tipo de una columna que contiene valores categóricos convirtiéndolo a nan.

    Args:
    df (pd.DataFrame): DF sobre el cual aplicamos los cambios.
    num_cols (list): lista de las variables que queremos convertir a numérica.

    Returns:
    pd.DataFrame: DF con los cambios realizados
    '''
    df_copy = df.copy()

    for col in num_cols:
        df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
    
    return df_copy 

def change_nulls_to_categoric(df, cat_cols):
    df_copy = df.copy()
    for col in cat_cols:
        df_copy.loc[df_copy[col].isna(), col] = 'NULO'

    return df_copy

def clean_completed(df, col_drop, nums, categ):
    df.drop(columns=col_drop, inplace=True)
    print(f'-> Columna "{col_drop}" eliminada ✅\n')
    print('***' *10)
    print('\n --> Procediendo a eliminar las filas duplicadas y las filas con más de la mitad de nulos\n')
    df_drop_duplicated_rows = clean_duplicated_thresh_nulls(df)
    print('\n Duplicados y filas eliminadas ✅\n')
    print('***' *10)
    print(f'\n --> Procediendo a cambiar el tipo de variable a numérica de {nums}')
    df_to_numeric = change_to_numeric(df_drop_duplicated_rows, nums)
    print('\n Variables cambiadas de tipo a numérica ✅\n')
    print('***' *10)
    print(f'\n --> Procediendo a cambiar los nulos a un valor categórico de las variables: {categ}')
    df_clean = change_nulls_to_categoric(df_to_numeric, categ)
    print('\n Valor NaN cambiadas de etiqueta ✅')
    return df_clean