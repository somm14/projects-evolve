import pandas as pd

from scipy.stats import skew, kurtosis

def describe_df(data:pd.DataFrame, umbral_categorica:int=10, umbral_continua:float=0.1, imprimir:bool=True) -> pd.DataFrame:
    '''
    Genera una descripción esquemática de las variables de un DataFrame, devolviendo un nuevo DataFrame en el que cada columna corresponde
    a una variable del conjunto de datos original y cada fila resume una propiedad básica y una clasificación sugerida de dicha variable.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame de entrada sobre el que se calcula la descripción de variables.
    umbral_categorica : int, defecto=10
        Umbral de cardinalidad absoluta para considerar una variable como categórica nominal.
    umbral_continua : float, defecto=0.1
        Umbral de cardinalidad relativa a partir del cual una variable numérica o temporal se considera continua.
    imprimir : bool, defecto=True
        Indica si se imprime por pantalla un resumen de los umbrales utilizados en la clasificación.

    Returns
    -------
    pandas.DataFrame
        DataFrame resumen que contiene, para cada variable del DataFrame original, su tipo de dato, número y porcentaje de valores nulos,
        cardinalidad absoluta y relativa, y una clasificación sugerida del tipo de variable.
    '''

    if not(isinstance(data, pd.DataFrame)):
        raise TypeError('La variable "data" debe ser de un DataFrame.')
    if not(isinstance(umbral_categorica, int)):
        raise TypeError('La variable "umbral_categorica" debe ser un número entero.')
    if not(isinstance(umbral_continua, (int, float))):
        raise TypeError('La variable "umbral_continua" debe ser un número.')
    if not(0 <= umbral_continua <= 1):
        raise ValueError('El valor de "umbral_continua" debe estar comprendido entre 0 y 1.')
    if not(isinstance(imprimir, bool)):
        raise TypeError('La variable "imprimir" debe ser True/False.')
    
    salida = {columna: [] for columna in data.columns}
    for columna in salida.keys():
        tipo = data[columna].dtype
        nulos = data[columna].isna().sum()
        cardinalidad = data[columna].nunique()
        clasificacion = 'Categorica'

        if cardinalidad == 2:
            clasificacion = 'Categorica_Binaria'

        elif cardinalidad <= umbral_categorica:
            clasificacion = 'Categorica'

        elif pd.api.types.is_numeric_dtype(tipo) or pd.api.types.is_datetime64_any_dtype(tipo):
            if cardinalidad / len(data) <= umbral_continua:
                clasificacion = 'Numerica_Discreta'
            else:
                clasificacion = 'Numerica_Continua'

        salida[columna].append(tipo)
        salida[columna].append(nulos)
        salida[columna].append(round(nulos / len(data) * 100, 1))
        salida[columna].append(cardinalidad)
        salida[columna].append(round(cardinalidad / len(data) * 100, 2))
        salida[columna].append(clasificacion)

    salida['Columnas'] = ['Tipo_Dato', 'Nulos', 'Nulos_%', 'Cardinalidad', 'Cardinalidad_%', 'Clasificacion_sugerida']

    if imprimir:
        print(f'Clasificación sugerida para {len(data):,} filas, con un umbral para categórica de {umbral_categorica\
                } sobre la cardinalidad y un umbral para númerica continua de {umbral_continua*100} % sobre la cardinalidad relativa.')
    return pd.DataFrame(salida).set_index('Columnas')

#####################################################################################################

def skew_kurt(df:pd.DataFrame, feature:list) -> None:
    '''
    Calcula la asimetría y la Curtosis de las variables numéricas.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame de entrada sobre el que se calcula la asimetría y la Curtosis.
    features : list
        Lista de las variables que queremos analizar

    Returns
    -------
    None
        Imprime por pantalla los resultados de ambos análisis
    '''
    # for col in features:
    asimetria = skew(df[feature])
    curtosis = kurtosis(df[feature])
    print(f'Analizando "{feature}":\n')

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