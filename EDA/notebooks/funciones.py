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