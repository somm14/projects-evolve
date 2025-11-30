import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


## PARA RELACIONAR UNA VARIABLE CATEGÓRICA CON UNA NUMÉRICA

def boxplot_cat_num(df, col_cat, col_num, orden_dict):
    '''
    Genera un boxplot para visualizar la relación entre una variable categórica y una variable numérica.

    Args:
    df (pd.DataFrame): DataFrame que contiene los datos.
    col_cat (str): Nombre de la columna categórica a usar en el eje x.
    col_num (str): Nombre de la columna numérica a usar en el eje y.
    orden_dict (dict): Diccionario con el orden lógico de categorías.

    Returns:
    None. Muestra directamente el gráfico con matplotlib/seaborn.
    '''

    df_copy = df.copy()

    if col_cat in orden_dict:
            orden = orden_dict[col_cat].copy()
    
    nulos = [cat for cat in df_copy[col_cat] if "NULO" in cat]
    no_nulos = [cat for cat in orden if cat not in nulos]

    nulos_ = list(set(nulos))
    orden_final = no_nulos + nulos_ if nulos_ else orden

    df_copy[col_cat] = pd.Categorical(df_copy[col_cat], categories=orden_final, ordered=True)

    plt.figure(figsize=(10,6))
    sns.boxplot(x=col_cat, y=col_num, data=df_copy)
    plt.title(f'Relación entre {col_num} y {col_cat}')
    plt.xlabel(f'Frecuencia de {col_cat}')
    plt.ylabel(f'Frecuencia de {col_num}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def violin_cat_num(df, col_cat, col_num, orden_dict):
    '''
    Genera un Violinplot para visualizar la relación entre una variable categórica y una variable numérica.

    Args:
    df (pd.DataFrame): DataFrame que contiene los datos.
    col_cat (str): Nombre de la columna categórica a usar en el eje x.
    col_num (str): Nombre de la columna numérica a usar en el eje y.
    orden_dict (dict): Diccionario con el orden lógico de categorías.

    Returns:
    None. Muestra directamente el gráfico con matplotlib/seaborn.
    '''

    df_copy = df.copy()

    if col_cat in orden_dict:
            orden = orden_dict[col_cat].copy()
    
    nulos = [cat for cat in df_copy[col_cat] if "NULO" in cat]
    no_nulos = [cat for cat in orden if cat not in nulos]

    nulos_ = list(set(nulos))
    orden_final = no_nulos + nulos_ if nulos_ else orden

    df_copy[col_cat] = pd.Categorical(df_copy[col_cat], categories=orden_final, ordered=True)

    plt.figure(figsize=(10,6))
    sns.violinplot(x=df_copy[col_cat], y=df_copy[col_num])    
    plt.title(f'Relación entre {col_num} y {col_cat}')
    plt.xlabel(f'Frecuencia de {col_cat}')
    plt.ylabel(f'Frecuencia de {col_num}')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_cartegoricas(df, col_cat1, col_cat2, orden_dict):
    '''
    Grafica dos variables categóricas con orden lógico si está definido en orden_dict.

    Args:
    df (pd.DataFrame): DataFrame con los datos.
    col_cat1 (str): Variable categórica del eje X.
    col_cat2 (str): Variable categórica usada como hue.
    orden_dict (dict): Diccionario con el orden lógico de categorías.

    Returns:
    None: Muestra una gráfica de barras analizando dos variables
    '''
    df_copy = df.copy()

    if col_cat1 in orden_dict:
        orden = orden_dict[col_cat1].copy()

        nulos = [cat for cat in df_copy[col_cat1] if "NULO" in cat]
        no_nulos = [cat for cat in orden if cat not in nulos]

        nulos_ = list(set(nulos))

        orden_final = no_nulos + nulos_ if nulos_ else orden
        df_copy[col_cat1] = pd.Categorical(df_copy[col_cat1], categories=orden_final, ordered=True)

    if col_cat2 in orden_dict:
        orden = orden_dict[col_cat2].copy()

        nulos = [cat for cat in df_copy[col_cat2] if "NULO" in cat]
        no_nulos = [cat for cat in orden if cat not in nulos]

        nulos_ = list(set(nulos))

        orden_final = no_nulos + nulos_ if nulos_ else orden
        df_copy[col_cat2] = pd.Categorical(df_copy[col_cat2], categories=orden_final, ordered=True)

    plt.figure(figsize=(10,6))
    sns.countplot(data=df_copy, x=col_cat1, hue=col_cat2)
    plt.title(f'Relación entre {col_cat1} y {col_cat2}')
    plt.xlabel(f'{col_cat1}')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=90)
    plt.legend(title=f'{col_cat2}')
    plt.tight_layout()
    plt.show()