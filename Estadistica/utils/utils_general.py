import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import skew, kurtosis

def card_tipo(df, umbral_categoria = 10, umbral_continua = 30):
    '''
    Tipifica las variables a categóricas, binarias, numéricas continuas o numéricas discretas dependiendo
    de un umbral dado.

    Argumentos:
    df[DataFrame]: Dataframe original sobre el que quiero trabajar.
    umbral_categoria[int]: Umbral límite para asignar que una variable es categórica. Por defecto, 10.
    umbral_continua[int]: Umbral mínimo para asignar que una variable es numérica binaria. Si no es 
    discreta. Por defecto, 30.

    Retorno:
    df_temp[DataFrame]: Dataframe con los resultados.
    '''
    df_temp = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad y porcentaje de variación de cardinalidad
    df_temp = df_temp.T
    df_temp = df_temp.rename(columns = {0: "Unique_values", 1: "%_Card", 2: "Tipo"})

    df_temp.loc[df_temp.Unique_values == 1, "%_Card"] = 0.00

    df_temp["tipo_sugerido"] = "Categorica"
    df_temp.loc[df_temp["Unique_values"] == 2, "tipo_sugerido"] = "Binaria"
    df_temp.loc[df_temp["Unique_values"] >= umbral_categoria, "tipo_sugerido"] = "Numerica discreta"
    df_temp.loc[df_temp["%_Card"] >= umbral_continua, "tipo_sugerido"] = "Numerica continua"

    return df_temp

def cols_observation(df, cols = []):
    '''
    Observación de columnas para ver el conteo de sus valores y los valores únicos.
    
    Argumentos:
    df[DataFrame]: Dataframe original sobre el que quiero trabajar.
    cols[list]: Lista de columnas con los que quiero hacer la observación.

    Retorna:
    Prints de las observaciones hechas
    '''
    cols_obs = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'pickup_hour', 'improvement_surcharge']
    for col in cols:
        print(f'Para "{col}":\n')
        print(f'Nulos:\n{df[col].isna().sum()}\n')
        if df[col].isna().sum() > 0:
            print(f'Porcentaje de nulos:\n{(df[col].isna().sum()/len(df)) * 100}')
        print(f'Valores:')
        print(df[col].value_counts(),'\n')
        print(f'Valores únicos:\n{df[col].unique()}')
        print('*'*20)


def skew_kurt(df, features):
    '''
    Calcula la asimetría y la Curtosis de las variables numéricas.

    Argumentos:
    df[DataFrame]: Dataframe original sobre el que quiero trabajar.
    features[list]: Lista de las variables que queremos analizar

    Retorna:
    Tupla de variables con listas de columnas clasificadas según su análisis

    '''
    for col in features:
        asimetria = skew(df[col])
        curtosis = kurtosis(df[col])
        print(f'Analizando "{col}":\n')

        if asimetria < 0:
            print(f'Asimetría -> {round(asimetria, 2)}')
            print('\tEsta variable tiene una asimetría negativa')
            print('\tEsta sesgada hacia la izquierda')

        elif 0 <= asimetria < 1:
            print(f'Asimetría -> {round(asimetria, 2)}')
            print('\tEsta variable tiene una distribución más o menos simétrica')

        else:
            print(f'Asimetría -> {round(asimetria, 2)}')
            print('\tEsta variable tiene una asimetría positiva')
            print('\tEsta sesgada hacia la derecha')
        
        if curtosis < 0:
            print(f'Curtosis -> {round(curtosis, 2)}')
            print('\tEsta variable tiene una distribución plana')

        elif 0 <= curtosis < 1:
            print(f'Curtosis -> {round(curtosis, 2)}')
            print('\tEsta variable tiene una distribución más o menos gaussiana')

        else:
            print(f'Curtosis -> {round(curtosis, 2)}')
            print('\tEsta variable tiene una distribución más picuda')
            print('\tProbabilidad alta de outliers')

        print('-'*50,'\n')

