import matplotlib.pyplot as plt
import seaborn as sns

## VISUALIZACIÓN DE VARIABLES INDIVIDUALES (Rescatada de utilidades del Bootcamp que realicé anteriormente adaptada a este DF)

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

        total = df[col].value_counts().sum()
        serie = round(df[col].value_counts().apply(lambda x: x / total), 2)

        if col in orden_categorias:
            orden = orden_categorias[col]
            categorias = serie.index.tolist()
            categorias_ordenadas = [cat for cat in orden if cat in categorias]
            if 'NULOS' in serie.index or None in serie.index:
                categorias_ordenadas.append('NULOS')

            serie = serie.reindex(categorias_ordenadas)

        # Gráfica
        if col == 'estado':  # HORIZONTAL
            sns.barplot(x=serie, y=serie.index, ax=ax, palette="viridis", hue = serie.index, legend = False)
            ax.set_xlabel("Frecuencia Relativa")
            ax.set_ylabel("")
        else:  # VERTICAL
            sns.barplot(x=serie.index, y=serie, ax=ax, palette="viridis", hue = serie.index, legend = False)
            ax.set_ylabel("Frecuencia Relativa")
            ax.tick_params(axis="x", rotation=90)

        ax.set_title(f"Distribución de {col}")

        # Mostrar valores
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
                    # vertical y soporta muchas categorías → texto vertical
                    height = p.get_height()
                    ax.annotate(
                        f"{height}",
                        (p.get_x() + p.get_width() / 2., height),
                        ha="center",
                        va="bottom",
                        #rotation=90,    # <-- aquí está la mejora
                        xytext=(0, 3),
                        textcoords="offset points"
                    )

    # Ocultar ejes vacíos
    for j in range(i + 1, num_filas * 2):
        axes[j].axis("off")

    plt.tight_layout()
    plt.show()

