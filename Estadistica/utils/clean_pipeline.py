import numpy as np
import pandas as pd

def map_cities(df_origin, df_map, right_on, merge_cols = [], cols_origin = []):
    '''
    Mapea códigos de ciudades haciendo un merge en el DF original.

    Argumentos:
    df_origin[DataFrame]: Dataframe original sobre el que quiero trabajar.
    df_map[DataFrame]: DataFrame con lo que representa el código de las ciudades.
    right_on[str]: String con el nombre de la variable con la que quiero unir el df_map.
    merge_cols[list]: Lista de columnas con los que quiero hacer el merge al DF original.
    cols_origin[list]: Lista de columnas con los que quiero hacer el merge con df_map.

    Retorna:
    df[DataFrame]: Dataframe con las trasnformaciones

    '''
    df_copy = df_origin.copy()
    rename_cols = ['PU_city', 'DO_city']
    for col, name in zip(cols_origin, rename_cols):
        df_copy = df_copy.merge(df_map[merge_cols], how='left', right_on=df_map[right_on], left_on=df_origin[col])
        df_copy.rename(columns={'Zone':name}, inplace=True)
        df_copy.drop(['key_0','LocationID', col], axis=1, inplace=True)
    df_copy.rename({'Borough_x': 'PU_Borough', 'Borough_y': 'DO_Borough'}, axis=1, inplace=True)
    return df_copy

def changes_date(df, cols_delete, cols_trans):
    '''
    Procesa aquellas variables que se quiere cambiar de tipo de dato y eliminar variables del dataset

    Argumentos:
    df[DataFrame]: Dataframe sobre el que quiero trabajar.
    cols_delete[str]: Lista de columnas que quiero eliminar.
    cols_trans[str]: Lista de columnas que quiero transformar.

    Retorna:
    df[DataFrame]: Dataframe con las trasnformaciones
    '''
    df[cols_trans] = pd.to_datetime(df[cols_trans])
    df.drop(cols_delete, axis=1, inplace=True)

    return df


def decoding_data(df, cols=[]):
    '''
    Mapea valores para conversión a variables categóricas

    Argumentos:
    df[DataFrame]: Dataframe sobre el que quiero trabajar.
    col[list]: Columna que quiero transformar

    Retorna:
    df[DataFrame]: Dataframe con las trasnformaciones

    '''
    for col in cols:
        if col is 'VendorID':
            valores = {1: 'Creative Mobile Technologies',
                       2: 'Curb Mobility',
                       6: 'Myle Technologies Inc'}
            df['provider'] = df[col].map(valores)
            df.drop(col, axis=1, inplace=True)
        if col is 'RatecodeID':
            valores = {1: 'Estándar',
                       2: 'JFK',
                       3: 'Newark',
                       4: 'Nassau o Westchester',
                       5: 'Negotiated fare',
                       99: np.nan}
            df['tariff_type'] = df[col].map(valores)
            df.drop(col, axis=1, inplace=True)
        if col is 'payment_type':
            valores = {0: 'Viaje con tarifa flexible',
                       1: 'Tarjeta de crédito',
                       2: 'Efectivo',
                       3: 'Sin cargo',
                       4: 'Disputa'}
            df[col] = df[col].map(valores)

    return df

def nuls(df, cols = []):
    '''
    Trata nulos en la columna 'Airport_fee'

    Parametres
    ----------
    df[DataFrame]: Dataframe sobre el que quiero trabajar.
    col[list]: Columna que quiero transformar

    Returns
    -------
    df[DataFrame]: Dataframe con las trasnformaciones
    '''
    for col in cols:
        if col is 'Airport_fee':
            df.loc[(df['Airport_fee'].isna()) & (df['PU_city'].isin(['LaGuardia Airport', 'JFK Airport'])), 'Airport_fee'] = 1.75            
            df.loc[(df['Airport_fee'].isna()) & (df['DO_city'].isin(['LaGuardia Airport', 'JFK Airport'])),'Airport_fee'] = 1.75
            df.loc[(df['Airport_fee'].isna()) & (~df['PU_city'].isin(['LaGuardia Airport', 'JFK Airport'])) & (~df['DO_city'].isin(['LaGuardia Airport', 'JFK Airport'])),'Airport_fee'] = 0
    
        if col is 'tariff_type':
            df.loc[(df['tariff_type'].isna()) & (df['DO_city'] == 'JFK Airport'), 'tariff_type'] = 'JFK'
            df.loc[(df['tariff_type'].isna()) & ~(df['DO_city'] == 'JFK Airport'), 'tariff_type'] = 'Estándar'

    return df


def data_transform(df, df_map):
    '''
    Pipeline que procesa todas las transformacioes necesarias del dataset.

    Argumentos:
    df[DataFrame]: Dataframe sobre el que quiero trabajar.
    df_map[DataFrame]: DataFrame con lo que representa el código de las ciudades.

    Retorna:
    df[DataFrame]: Dataframe con las trasnformaciones
    '''
    df_date = changes_date(df, ['tpep_dropoff_datetime', 'is_weekend'], 'tpep_pickup_datetime')

    df_merge = map_cities(df_date, df_map, right_on='LocationID', merge_cols=['LocationID', 'Zone', 'Borough'], cols_origin=['PULocationID', 'DOLocationID'])
    
    df_cod = decoding_data(df_merge, ['VendorID', 'RatecodeID', 'payment_type'])

    df_no_nuls = nuls(df_cod, ['Airport_fee', 'tariff_type'])

    return df_no_nuls