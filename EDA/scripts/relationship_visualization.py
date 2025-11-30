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

## PARA RELACIONAR UNA VARIABLE CATEGÓRICA CON OTRA CATEGÓRICA
 
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


## PARA RELACIONAR TRES VARIABLES: DOS CATEGÓRICAS CON UNA NUMÉRICA

def boxplot_trivariante(df, col1, col2, hue, orden_dict):
    '''
    Grafica 3 variables: 2 categóricas con orden lógico si está definido en orden_dict y una numérica.

    Args:
    df (pd.DataFrame): DataFrame con los datos.
    col1 (str): Variable categórica del eje X.
    col2 (str): Variable numérica del eje y.
    hue (str): Variable categórica usada como hue.
    orden_dict (dict): Diccionario con el orden lógico de categorías.

    Returns:
    None: Muestra una gráfica de cajas analizando tres variables
    '''
    plt.figure(figsize=(14, 8))

    df_copy = df.copy()

    list_cols = [col1, col2, hue]

    for col in list_cols:
        if df_copy[col].dtype == 'O':
            if col in orden_dict:
                orden = orden_dict[col].copy()
            
            nulos = [cat for cat in df_copy[col] if "NULO" in cat]
            no_nulos = [cat for cat in orden if cat not in nulos]

            nulos_ = list(set(nulos))
            orden_final = no_nulos + nulos_ if nulos_ else orden

            df_copy[col] = pd.Categorical(df_copy[col], categories=orden_final, ordered=True)


    sns.boxplot(
        data=df,
        x=col1,
        y=col2,
        hue=hue
    )

    # 2. Mover la leyenda afuera de la gráfica
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title=hue, borderaxespad=0)

    # 3. Rotar etiquetas de abajo si se solapan
    plt.xticks(rotation=45)

    # 4. Título y etiquetas claras
    plt.title(f"Relación entre {col1}, {col2} y {hue}")
    plt.xlabel(f" {col1}")
    plt.ylabel(f"Frecuencia {col2}")

    # 5. Ajuste final IMPORTANTE (con paréntesis)
    plt.tight_layout()

    plt.show()

def heatmap_trivariante(df, col_filas, col_columnas, col_valores, diccionario_orden):
    '''
    Genera un heatmap ordenado según un diccionario de categorías predefinido.

    Parámetros:
    df (pd.DataFrame): DataFrame con los datos.
    col_filas (str): Nombre de la columna para el eje Y (filas).
    col_columnas (str): Nombre de la columna para el eje X (columnas).
    col_valores (str): Variable numérica para calcular la mediana.
    diccionario_orden (dict): Diccionario {nombre_columna: [lista_ordenada]}.

    Returns:
    None: Heatmap de la relación entre 2 categóricas y una numérica
    '''

    tabla = df.pivot_table(
        index=col_filas,
        columns=col_columnas,
        values=col_valores,
        aggfunc='median'
    )

    if col_filas in diccionario_orden:
        orden_deseado = diccionario_orden[col_filas]
        # Filtramos para quedarnos solo con las categorías que existen en los datos actuales
        orden_valido = [x for x in orden_deseado if x in tabla.index]
        tabla = tabla.reindex(orden_valido)

    if col_columnas in diccionario_orden:
        orden_deseado = diccionario_orden[col_columnas]
        orden_valido = [x for x in orden_deseado if x in tabla.columns]
        tabla = tabla.reindex(columns=orden_valido)

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        tabla, 
        annot=True, 
        fmt=".1f", 
        cmap="YlGnBu", 
        linewidths=.5
    )

    plt.title(f"Mediana de {col_valores}\n({col_filas} vs {col_columnas})")
    plt.xlabel(col_columnas)
    plt.ylabel(col_filas)
    plt.xticks(rotation=90, ha='right')
    plt.yticks(rotation=0, ha='right')
    plt.tight_layout() 
    plt.show()
