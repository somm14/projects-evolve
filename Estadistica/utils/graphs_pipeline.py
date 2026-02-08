import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_combined_graphs(df, columns, whisker_width=1.5, bins = None):
    '''
    Grafica combinación de histogramas + KDE y Boxplots (con límite con IQR) para analizar
    la distribución de las variables numéricas

    Parametrers
    ----------
    df[DataFrame]: DataFrame que quiero analizar.
    columns[list or str]: Variables los cuales quiero analizar.
    whisker_width[int]: Umbral del tamaño del bigote del boxplot. Por defecto, 1.5
    bins[int]: Número de bins del histograma. Por defecto, None

    Returns:
    --------
    Subplots de histogramas y boxplots
    
    '''
    num_cols = len(columns)
    if num_cols:
        
        fig, axes = plt.subplots(num_cols, 2, figsize=(12, 5 * num_cols))
        stats = {}

        for i, column in enumerate(columns):
            if df[column].dtype in ['int64', 'float64']:
                # Histograma y KDE
                sns.histplot(df[column], kde=True, ax=axes[i,0] if num_cols > 1 else axes[0], bins= "auto" if not bins else bins)
                if num_cols > 1:
                    axes[i,0].set_title(f'Histograma y KDE de {column}')
                else:
                    axes[0].set_title(f'Histograma y KDE de {column}')

                # Boxplot
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

                stats[column] = {
                    "Q1": Q1,
                    "Q3": Q3,
                    "IQR": IQR,
                    "Lower": lower_bound,
                    "Upper": upper_bound,
                    "Outliers": len(outliers)
                }

                sns.boxplot(x=df[column], ax=axes[i,1] if num_cols > 1 else axes[1], whis=whisker_width)
                axes[i,1].axvline(lower_bound, color='red', linestyle='--', label='Lower bound')
                axes[i,1].axvline(upper_bound, color='red', linestyle='--', label='Upper bound')
                
                if num_cols > 1:
                    axes[i,1].set_title(f'Boxplot de {column}')
                else:
                    axes[1].set_title(f'Boxplot de {column}')

        plt.tight_layout()
        plt.show()

        for col, s in stats.items():
            print(f"\n--- {col} ---")
            print("Q1:", round(s["Q1"], 2))
            print("Q3:", round(s["Q3"], 2))
            print("IQR:", round(s["IQR"], 2))
            print("Lower bound:", round(s["Lower"], 2))
            print("Upper bound:", round(s["Upper"], 2))
            print("Número de outliers:", round(s["Outliers"], 2))

def var_graph(df, group):
    var_by_duration = (df.groupby(group[0])[group[1]].var())

    sns.lineplot(x=var_by_duration.index, y=var_by_duration.values)
    plt.xlabel(f"{group[0]}")
    plt.ylabel(f"Varianza {group[1]}")
    plt.title(f"Varianza de {group[1]} según {group[0]}")
    plt.show()

def corr_num(df, features_num):
    matriz_corr = df[features_num].corr()

    plt.figure(figsize=(10, 10))

    sns.heatmap(matriz_corr, annot=True, cmap='coolwarm')
    plt.tight_layout()
    plt.show()

    var_corr = []
    for var in matriz_corr:
        if var == 'total_amount':
            for var_num, corr in zip(matriz_corr.index, matriz_corr[var]):
                if 1 > corr > 0.5:
                    var_corr.append(var_num)
                elif -1 < corr < -0.5:
                    var_corr.append(var_num)

    return var_corr, matriz_corr

def grafico_dispersion_con_correlacion(df, columna_x, columna_y, tamano_puntos=50, mostrar_correlacion=False):
    """
    Crea un diagrama de dispersión entre dos columnas y opcionalmente muestra la correlación.

    Args:
    df (pandas.DataFrame): DataFrame que contiene los datos.
    columna_x (str): Nombre de la columna para el eje X.
    columna_y (str): Nombre de la columna para el eje Y.
    tamano_puntos (int, opcional): Tamaño de los puntos en el gráfico. Por defecto es 50.
    mostrar_correlacion (bool, opcional): Si es True, muestra la correlación en el gráfico. Por defecto es False.
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columna_x, y=columna_y, s=tamano_puntos)

    if mostrar_correlacion:
        correlacion = df[[columna_x, columna_y]].corr().iloc[0, 1]
        plt.title(f'Diagrama de Dispersión con Correlación: {correlacion:.2f}')
    else:
        plt.title('Diagrama de Dispersión')

    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.grid(True)
    plt.show()

def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values=False, measure='mean'):
    # Calcula la medida de tendencia central (mean o median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        # Por defecto, usa la media
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Ordena los valores
    grouped_data = grouped_data.sort_values(ascending=False)

    # Si hay más de 7 categorías, las divide en grupos de 7
    if grouped_data.shape[0] > 7:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / 7))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * 7:(i + 1) * 7]
            data_subset = grouped_data.loc[categories_subset]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=data_subset.index, y=data_subset.values)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {categorical_col} y {numerical_col} - Grupo {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, 7),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de 5 categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=grouped_data.index, y=grouped_data.values)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {categorical_col} y {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()


def pinta_distribucion_categoricas(df, columnas_categoricas, relativa=False, mostrar_valores=False):
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(15, 5 * num_filas))
    axes = axes.flatten() 

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]
        if relativa:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            serie = df[col].value_counts()
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()



def distribucion_categorica_relativa(df, col_cat):
    plt.figure(figsize=(10,10))

    total = df[col_cat].value_counts().sum()
    serie = df[col_cat].value_counts().apply(lambda x: x/total)
    sns.barplot(x=serie.index, y=serie, palette='viridis', hue=serie.index, legend=False)
    plt.ylabel('Frecuencua Relativa')