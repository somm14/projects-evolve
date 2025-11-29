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
    print('\nNúmero de registros en el DF sin duplicados ->', len_sin_thresh)

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

def change_nulls_from_categoric(df, cat_cols, fill_value='NULO'):
    '''
    Rellena NaNs únicamente en las columnas categóricas pasadas con el valor `fill_value`.
    No modifica columnas numéricas.

    Args:
    df (pd.DataFrame): DF sobre el cual aplicamos los cambios.
    cat_cols (list): lista de las variables que queremos tranformar.
    fill_value (str): str con el que queremos rellenar los NaNs. Por defecto 'NULO'

    Returns:
    pd.DataFrame: DF con los cambios realizados

    '''
    df_copy = df.copy()
    for col in cat_cols:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].fillna(fill_value)
    return df_copy

def categorize_sueño_h(df, sueño_col='sueño_h'):
    '''
    - Convierte sueño_h a numérico (coerce).
    - Crea una columna categórica con rangos:
       - 'Menos de 4h'
       - 'Entre 4 y 7h'
       - 'Más de 7h'

    Args:
    df (pd.DataFrame): DF sobre el cual aplicamos los cambios.
    sueño_col (str): variable sobre el que se quiere hacer la categorización. Por defecto es 'sueño_h'

    Returns:
    pd.DataFrame: DF con los cambios realizados
    '''
    df_copy = df.copy()

    df_copy[sueño_col] = pd.to_numeric(df_copy[sueño_col], errors='coerce')

    df_copy.loc[df_copy[sueño_col] < 4, 'sueño_cat'] = 'Menos de 4h'
    df_copy.loc[(df_copy[sueño_col] >= 4) & (df_copy[sueño_col] <= 7), 'sueño_cat'] = 'Entre 4 y 7h'
    df_copy.loc[df_copy[sueño_col] > 7, 'sueño_cat'] = 'Más de 7h'
    df_copy.loc[df_copy[sueño_col].isna(), 'sueño_cat'] = np.nan

    return df_copy



def clean_completed(df, col_drop):
    '''
    Pipeline de limpieza:
        - Eliminar columnas en col_drop
        - Eliminar duplicados (manteniendo la primera)
        - Eliminar filas con más de la mitad de valores nulos
        - Categorizar 'sueño_h' en rangos y etiquetar NaNs
        - Convertir dos columnas a numéricas: 'salud_mental_malos', 'salud_fisica_mala'
        - Convertir el resto de variables con NaNs (solo categoricas) a 'NULO'

    Args:
      df (pd.DataFrame)
      col_drop (str): columna a eliminar

     Returns:
     tuple: Una tupla con 3 variables: 
        - [0] (list): listado de las variables numéricas
        - [1] (list): listado de las variables categóricas
        - [2] (pd.DataFrame): DF con la limpieza realizada
    '''

    
    df.drop(columns=col_drop, inplace=True)
    print(f'-> Columna "{col_drop}" eliminada ✅\n')
    print('***' *10)
    
    print('\n\t --> Procediendo a eliminar las filas duplicadas y las filas con más de la mitad de nulos\n')
    df_drop_duplicated_rows = clean_duplicated_thresh_nulls(df)
    print('\n Duplicados y filas eliminadas ✅\n')
    print('***' *10)

    print('\n\t --> Procediendo a categorizar los valores de la coluna "sueño_h":\n')
    df_change_sueño = categorize_sueño_h(df_drop_duplicated_rows)
    print('\n Variable categorizada ✅\n')
    print('***' *10)
    
    numeric_cols = ['salud_mental_malos', 'salud_fisica_mala']
    categorical_cols = [c for c in df_change_sueño.columns if c not in numeric_cols]
    
    print(f'\n-> Columnas numéricas detectadas (a convertir): {numeric_cols}')
    print('\n\t --> Procediendo a cambiar el tipo de variable a numérica:')
    df_to_numeric = change_to_numeric(df_change_sueño, numeric_cols)
    print('\n Variables cambiadas de tipo a numérica ✅\n')
    print('***' *10)

    print(f'\n-> Columnas categóricas detectadas (para rellenar NaNs): {categorical_cols}')
    print('\n\t --> Procediendo a cambiar los nulos a un valor categórico:')
    df_clean = change_nulls_from_categoric(df_to_numeric, categorical_cols)
    print('\n Valor NaN cambiadas de etiqueta ✅')
    return numeric_cols, categorical_cols, df_clean