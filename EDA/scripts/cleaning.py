import pandas as pd
import numpy as np

def ordenar_cat(df, cols_cat, orden):
    '''
    Función para ordenar visualmente los valores de las variables categóricas ya que no tiene un orden con el que se pueda hacer sorted().

    Args:
    df (pd.DataFrame): DF desde el cual queremos recoger la información
    cols_cat (list): lista de los nombres de las variables categóricas
    orden (dict): diccionario del orden de los valores de cada variable.
    frecuencia_relativa (bool): Si se quiere mostrar la frecuencia relativa. Por defecto, False.

    Returns:
    None: imprime el value_counts() de cada variable con sus valores ordenados de manera lógica.
    '''
    for col in cols_cat:
        serie = df[col].value_counts()
        if col in orden:
            orden_ = orden[col]
            categorias = serie.index.tolist()
            categorias_ordenadas = [cat for cat in orden_ if cat in categorias]
            if 'NULOS' in serie.index or None in serie.index:
                categorias_ordenadas.append('NULOS')

            serie = serie.reindex(categorias_ordenadas)
            print(serie)
            print('***' * 10)

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


def clean_nulls(df, cat_cols):
    df_copy = df.copy()
    nuls_prc = df_copy.isna().sum() / len(df_copy) * 100
    for col, prc in zip(nuls_prc.index, nuls_prc):
        try:
            if prc >= 40:
                print(f'\nSe elimina la variable "{col}"')
                df_copy.drop(columns=col, inplace=True)
            elif 2 < prc < 15:
                if col in cat_cols:
                    print(f'\nLa variable "{col}" tiene {round(prc, 4)}% de nulos por lo que cambiamos sus valores Desconocidos por "Unknown"')
                    df_copy[col] = df_copy[col].replace(['Don’t know/Not sure', 'Refused', np.nan], 'Unknown')
                else:
                    print(f'\nLa variable "{col}" tiene {round(prc, 4)}% de nulos por lo que cambiamos sus valores Desconocidos por "NaN"')
                    df_copy[col] = df_copy[col].replace(['Don’t know/Not sure', 'Refused'], np.nan)
                    df_copy[col] = df_copy[col].astype(float)
            elif 0 < prc < 1.9:
                if col in cat_cols:
                    print(f'\nLa variable "{col}" tiene {round(prc, 4)}% de nulos por lo que transformamos sus valores Desconocidos por la moda')
                    df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
                else:
                    print(f'\nLa variable "{col}" tiene {round(prc, 4)}% de nulos por lo que tranformamos sus valores Desconocidos por la mediana')
                    df_copy[col] = df_copy[col].replace(['Don’t know/Not sure', 'Refused'], np.nan)
                    df_copy[col] = df_copy[col].astype(float)
                    df_copy[col] = df_copy[col].fillna(df_copy[col].median())
            else:
                print(f'\nLa variable "{col}" tiene {round(prc, 2)}% de nulos por lo que no se transforma ninguno de sus valores')

        except Exception as e:
            print(e)
            continue

    return df_copy