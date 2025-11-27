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