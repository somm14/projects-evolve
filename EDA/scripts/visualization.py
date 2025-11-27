import matplotlib.pyplot as plt
import seaborn as sns

## VISUALIZACIÓN DE VARIABLES INDIVIDUALES (Rescatada de utilidades del Bootcamp que realicé anteriormente adaptada a este DF)

def distribucion_categoricas(df, columnas_categoricas):
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
        
        if col == 'estado':
            serie = df[col].value_counts()
            sns.barplot(x=serie, y=serie.index, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')
        else:
            serie = df[col].value_counts()
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')

    
        if col == 'estado':
            ax.set_title(f'Distribución de {col}')
            ax.set_ylabel('')
            ax.set_xlabel('')
            ax.tick_params(axis='x', rotation=90)
        
        else:
            ax.set_title(f'Distribución de {col}')
            ax.set_xlabel('')
            ax.tick_params(axis='x', rotation=90)

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()