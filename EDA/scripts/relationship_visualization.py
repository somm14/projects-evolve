import matplotlib.pyplot as plt
import seaborn as sns

def boxplot_cat_num(df, col_cat, col_num):
    '''
    Genera un boxplot para visualizar la relación entre una variable categórica y una variable numérica.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        col_cat (str): Nombre de la columna categórica a usar en el eje x.
        col_num (str): Nombre de la columna numérica a usar en el eje y.

    Returns:
    None. Muestra directamente el gráfico con matplotlib/seaborn.
    '''

    plt.figure(figsize=(10,6))
    sns.boxplot(x=col_cat, y=col_num, data=df)
    plt.title(f'Relación entre {col_num} y {col_cat}')
    plt.xlabel(f'Frecuencia de {col_cat}')
    plt.ylabel(f'Frecuencia de {col_num}')
    plt.xticks(rotation=45)
    plt.show()


def plot_cartegoricas(df, col_cat1, col_cat2):
    plt.figure(figsize=(10,6))
    sns.countplot(data=df, x=col_cat1, hue=col_cat2)
    plt.title(f'Relación entre {col_cat1} y {col_cat2}')
    plt.xlabel('')
    plt.ylabel('Cantidad')
    plt.legend(title='Categoría 2')
    plt.show()