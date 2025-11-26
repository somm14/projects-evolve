import numpy as np
## FUNCIONES PARA CARGAR Y REFACTORIZAR EL DATASET ORIGINAL

def ranges_expand(mapping):
    '''
    Función para expandir los ranges de los diccionarios para mapear el DF original

    Args:
    mapping (dict): diccionario único donde están guardadas las variables del DF que se quiere mapear

    Returns:
    dict: Diccionario donde están los ranges expandidos y así se pueda mapear con el DF original.
    '''
    dict_expand = {}
    for k,v in mapping.items():
        if isinstance(k, range):
            for i in k:
                dict_expand[i] = v
        else:
            dict_expand[k] = v
    return dict_expand


def mapeo_df_original(df, modulo):
    '''
    Esta función mapea los valores codificados del dataset crudo.

    Args:
    df (pd.DataFrame): DF del dataset crudo.
    modulo (module): módulo donde se encuentra el script que queremos utilizar para realizar el mapeo.

    Returns:
    pd.DataFrame: Df mapeado y descodificado. 
    
    '''

    # Sacar las variables del archivo .py
    variables_ = [var for var in dir(modulo) if not var.startswith('_')]
    
    # Guardo todas las variables y su contenido dentro de un diccionario único.
    mapeo = {}
    for var in variables_:
        valor_variable = getattr(modulo, var)    
        if valor_variable is np:
            continue 
        for col, valor in valor_variable.items():
            mapeo[col] = valor
        
    # Expando los ranges
    mappings = {col: ranges_expand(map_dict) for col, map_dict in mapeo.items()}

    # Mapeo en el DF original
    df_1 = df.copy()

    for col, m in mappings.items():
        df_1[col] = df_1[col].apply(lambda x: m.get(x, x)) # Uso lambda para que me cambie aquellos valores que están en el dict para que algunos valores me lo deje como están.

    # Instancio las columnas seleccionadas previamente
    cols = mappings.keys()
    df_1 = df_1[cols]

    # Lo guardo en csv
    df_1.to_csv('./data/mapped_data.csv', index=False)
    
    return df_1