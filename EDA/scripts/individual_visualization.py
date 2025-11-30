import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

## VISUALIZACIÓN SIN GRÁFICAS DE todo EL DF

def visualizacion_general(df):
    '''
    Función que visualiza de manera general:
        - El tipo de datos que hay en el DF
        - Divide por columnas la cantidad de registros que hay por cada valor
        - La cantidad de valores únicos por cada variable.

    Args:
    df (pd.DataFrame): DF sobre el que se quiere hacer la visualización

    Returns:
    None: imprime por pantalla los resultados que queremos obtener: tipo de datos, cantidad por cada valor y cantidad de valores únicos
    '''
    print('Tipo de variables de todo el DF:\n')
    print(df.dtypes, '\n')
    print('***'*10,'\n')

    for col in df.columns:
        print(f'--> Analizando la variable "{col}"\n')
        print('\nCantidad de registros por cada valor:\n')
        print(df[col].value_counts(dropna=False),'\n')
        print('\nNúmero de valores únicos:', df[col].nunique(),'\n')
        print('***'*10,'\n')


def visualizacion_duplicados(df):
    '''
    Función para visualizar:
        - Duplicados de un DF
        - Nulos con y sin duplicados
        - Diferencia entre ambos

    Args:
    df (pd.DataFrame): DF sobre el que se quiere hacer la visualización

    Returns:
    None: imprime por pantalla los resultados que queremos obtener.

    '''
    print(f'-> Número total de duplicados en el DF: {df.duplicated(keep=False).sum()}\n')
    df_dup = df[df.duplicated(keep=False)]
    nan_dup = df_dup.isna().sum()
    nan_df = df.isna().sum()
    dif_nulos = nan_df - nan_dup
    print(f'-> Nulos en el DF de duplicados:\n\n{nan_dup}\n')
    print(f'\n-> Nulos en el DF completo:\n\n{nan_df}\n')
    print(f'\n-> Diferencia entre ambos:\n\n{dif_nulos}\n')
    print(f'\n-> Número de nulos sin tener en cuenta la primera ocurrencia: {df.duplicated().sum()}')


## VISUALIZACIÓN DE VARIABLES INDIVIDUALES (Rescatadas de utilidades del Bootcamp que realicé anteriormente adaptada a este DF)

def distribucion_numericas(df, columns, whisker_width=1.5, bins = None):
    '''
    Función que visualiza sobre las variables numéricas, dos tipos de gráficas: histograma + KDE y BoxPlot

    Args:
    df (pd.DataFrame): DF sobre el que se quiere hacer la visualización
    columns (list): listado de columnas sobre las que quiero hacer las visualizaciones.
    whisker_width (float): longitud de los 'bigotes' del BoxPlot.
    bins (int/float): número de bins que queremos adjudicar al histograma. Por defecto NoNe y en la función se reflejaría 'auto'.

    Returns:
    Gráficos individuales mostrando la distribución de las variables númericas

    '''
    num_cols = len(columns)
    if num_cols:
        
        fig, axes = plt.subplots(num_cols, 2, figsize=(12, 5 * num_cols))
        print(axes.shape)

        for i, column in enumerate(columns):
            if df[column].dtype in ['int64', 'float64']:
                # Histograma y KDE
                sns.histplot(df[column], kde=True, ax=axes[i,0] if num_cols > 1 else axes[0], bins= "auto" if not bins else bins)
                if num_cols > 1:
                    axes[i,0].set_title(f'Histograma y KDE de {column}')
                else:
                    axes[0].set_title(f'Histograma y KDE de {column}')

                # Boxplot
                sns.boxplot(x=df[column], ax=axes[i,1] if num_cols > 1 else axes[1], whis=whisker_width)
                if num_cols > 1:
                    axes[i,1].set_title(f'Boxplot de {column}')
                else:
                    axes[1].set_title(f'Boxplot de {column}')

        plt.tight_layout()
        plt.show()



def distribucion_categoricas(df, orden_categorias, columnas_categoricas, mostrar_valores = False):
    '''
    Función para visualizar, mediante una gráfica de barras, las variables categóricas respecto a su frecuencia absoluta.

    Args:
    df (df.DataFrame): DF del cuál se obtiene la información.
    columnas_categoricas (list): Lista del nombre de las columnas categóricas de las que se quiere hacer la visualización
    
    Returns:
    Gráficos individuales mostrando la distribución de las variables categóricas.
    '''
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(10, 10 * num_filas))
    axes = axes.flatten()

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]

        serie = df[col].value_counts(dropna=False)

        # Etiqueto los NaN a 'NULOS'
        serie.index = serie.index.map(lambda x: 'NULOS' if pd.isna(x) else x)

        # Ordeno las categorías
        if col in orden_categorias:
            orden = orden_categorias[col]
            categorias = serie.index.tolist()
            categorias_ordenadas = [cat for cat in orden if cat in categorias]
            if 'NULOS' in categorias:
                categorias_ordenadas.append('NULOS')

            serie = serie.reindex(categorias_ordenadas)

        if col == 'estado':  # HORIZONTAL
            sns.barplot(x=serie, y=serie.index, ax=ax, palette="Blues_d", hue = serie.index, legend = False)
            ax.set_xlabel("Frecuencia Relativa")
            ax.set_ylabel("")
        else: 
            sns.barplot(x=serie.index, y=serie, ax=ax, palette="Blues_d", hue = serie.index, legend = False)
            ax.set_ylabel("Frecuencia Relativa")
            ax.tick_params(axis="x", rotation=90)

        ax.set_title(f"Distribución de {col}")

        if mostrar_valores:
            for p in ax.patches:
                if col == "estado":
                    width = p.get_width()
                    y_pos = p.get_y() + p.get_height() / 2
                    ax.annotate(
                        f"{width}",
                        (width, y_pos),
                        ha="left",
                        va="center",
                        xytext=(5, 0),
                        textcoords="offset points"
                    )
                else:
                    height = p.get_height()
                    rotation = 0 if len(serie) <= 6 else 90  
                    ax.annotate(
                        f"{height}",
                        (p.get_x() + p.get_width() / 2., height/2),
                        ha="center",
                        va="bottom",
                        color="#E2CB8B",
                        rotation=rotation,
                        xytext=(0, 3),
                        textcoords="offset points"
                    )

    for j in range(i + 1, num_filas * 2):
        axes[j].axis("off")

    plt.tight_layout()
    plt.show()


def distribucion_sueño(df, col, titulo=None):
    """
    Muestra un barplot con la distribución de la variable categórica 'sueño_cat' con un orden lógico en las categorías.

    Args: 
    df (df.DataFrame): DF del cuál se obtiene la información
    col (srt): columna de la cual se quiere ver la distribución

    Returns:
    Gráfica de barras
    """

    orden_categorias = ["Menos de 4h", "Entre 4 y 7h", "Más de 7h", 'NULO']

    df[col] = pd.Categorical(df[col], categories=orden_categorias, ordered=True)

    counts = df[col].value_counts(dropna=False).sort_index()

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=counts.index.astype(str), y=counts.values, palette='viridis', hue=counts.index.astype(str), legend=False)

    for i, v in enumerate(counts.values):
        ax.text(i, v + (0.02 * max(counts.values)),
                str(v), ha='center', va='bottom',
                fontsize=10, color="#555555", fontweight="bold")

    plt.title(titulo if titulo else f"Distribución de {col}", fontsize=14)
    plt.xlabel(col)
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
