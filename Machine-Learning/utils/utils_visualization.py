import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.utils_description import skew_kurt

from sklearn.metrics import roc_curve, ConfusionMatrixDisplay


plt.style.use('ggplot')
sns.set_palette('husl')

def plot_num_swkr_iqr(df:pd.DataFrame, columns:list, whisker_width:int = 1.5, bins = None) -> None:
    """
    Grafica combinación de histogramas + KDE y Boxplots (con límite con IQR) para analizar
    la distribución de las variables numéricas

    Para cada columna en la lista, la función crea una fila con dos subgráficos:
    1. A la izquierda: Un histograma con una estimación de densidad de kernel (KDE).
    2. A la derecha: Un boxplot para visualizar la distribución y los valores atípicos.
    Además, llama a la función `skew_kurt` para mostrar métricas estadísticas.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos a graficar.
    columns : list of str
        Lista con los nombres de las columnas que se desean visualizar.
    whisker_width : float, optional
        La longitud de los bigotes del boxplot en términos de múltiplos del 
        rango intercuartílico (IQR). Por defecto es 1.5.
    bins : int or str, optional
        Número de contenedores para el histograma. Si es None, se utiliza 
        "auto". Por defecto es None.

    Returns
    -------
    None
        La función muestra los gráficos directamente usando plt.show().
    """
    num_cols = len(columns)
    if num_cols:
        
        fig, axes = plt.subplots(num_cols, 2, figsize=(12, 5 * num_cols))
        stats = {}

        for i, column in enumerate(columns):
            skew_kurt(df, column)
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

#####################################################################################################


def plot_categoricas(df:pd.DataFrame, columnas_categoricas:list, relativa:bool = False, mostrar_valores:bool = False) -> None:
    """
    Genera gráficos de barras para visualizar la distribución de variables categóricas.

    La función crea una cuadrícula de subgráficos (2 columnas por fila) mostrando las 10 categorías más frecuentes para cada variable especificada. 
    Permite alternar entre frecuencias absolutas y relativas, y añadir etiquetas de datos.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos.
    columnas_categoricas : list of str
        Lista de nombres de las columnas categóricas a graficar.
    relativa : bool
        Si es True, muestra la frecuencia relativa (proporción) en el eje Y. 
        Si es False, muestra el recuento total (frecuencia absoluta). 
        Por defecto es False.
    mostrar_valores : bool
        Si es True, añade etiquetas de texto sobre cada barra con el valor exacto 
        (frecuencia o proporción). Por defecto es False.

    Returns
    -------
    None
        La función despliega la figura con plt.show().
    """
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(15, 5 * num_filas))
    axes = axes.flatten() 

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]
        if relativa:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)[:10]
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            serie = df[col].value_counts()[:10]
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=90)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

#####################################################################################################

def plot_cat_num_histograms(df:pd.DataFrame, cat_col:str, num_col:str, group_size:int) -> None:
    """
    Genera histogramas comparativos con KDE, agrupando las categorías en lotes 
    para evitar la saturación visual.

    La función divide las categorías únicas de una columna en grupos de tamaño 
    definido y genera un gráfico independiente por cada grupo, facilitando la 
    comparación de la distribución de una variable numérica entre ellas.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos.
    cat_col : str
        Nombre de la columna categórica que define los grupos.
    num_col : str
        Nombre de la columna numérica cuya distribución se desea analizar.
    group_size : int
        Número máximo de categorías a mostrar simultáneamente en un solo gráfico.

    Returns
    -------
    None
        Despliega una serie de figuras de Matplotlib.
    """
    unique_cats = df[cat_col].unique()
    num_cats = len(unique_cats)

    for i in range(0, num_cats, group_size):
        subset_cats = unique_cats[i:i+group_size]
        subset_df = df[df[cat_col].isin(subset_cats)]
        
        plt.figure(figsize=(10, 6))
        for cat in subset_cats:
            sns.histplot(subset_df[subset_df[cat_col] == cat][num_col], kde=True, label=str(cat))
        
        plt.title(f'Histograms of {num_col} for {cat_col} (Group {i//group_size + 1})')
        plt.xlabel(num_col)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

#####################################################################################################

def plot_categorical_numerical_relationship(df:pd.DataFrame, categorical_col:str, numerical_col:list) -> None:
    """
    Genera gráficos de barras para analizar la relación entre una variable 
    categórica y múltiples variables numéricas.

    Para cada columna numérica proporcionada, la función crea un gráfico de barras 
    que muestra el valor agregado (por defecto la media) para cada categoría. 
    Incluye etiquetas automáticas sobre las barras con el valor calculado.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos de origen.
    categorical_col : str
        El nombre de la columna categórica que se utilizará en el eje X.
    numerical_col : list of str
        Una lista con los nombres de las columnas numéricas que se desean 
        analizar en el eje Y (se generará un gráfico independiente por cada una).

    Returns
    -------
    None
        La función muestra los gráficos de forma secuencial mediante plt.show().
    """
    for col in numerical_col:
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=df[categorical_col], y=df[col], errorbar=None)
        plt.title(f'Relación entre {categorical_col} y {col}')
        plt.xlabel(f'{categorical_col}')
        plt.ylabel(f'{col}')
        plt.xticks(rotation=45)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')
        plt.show()

#####################################################################################################

def plot_categorical_relationship(df:pd.DataFrame, cat_col1:str, cat_col2:list) -> None:
    """
    Analiza la relación entre una variable categórica principal y una lista de 
    otras variables categóricas mediante gráficos de conteo agrupados.

    Para cada variable en la lista `cat_col2`, la función identifica las 10 
    categorías más frecuentes y genera un `sns.countplot` segmentado por 
    la variable de referencia `cat_col1`.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos.
    cat_col1 : str
        Nombre de la columna categórica base (eje X), comúnmente utilizada 
        como variable objetivo o clasificación principal.
    cat_col2 : list of str
        Lista de nombres de columnas categóricas cuyos niveles se desean 
        comparar (utilizadas como 'hue' en el gráfico).

    Returns
    -------
    None
        Despliega los gráficos secuencialmente mediante plt.show().
    """
    for col in cat_col2:
        if col != cat_col1:
            # 1. Identificar las 10 categorías más frecuentes de la columna actual
            top_10_categories = df[col].value_counts().nlargest(10).index
            
            # 2. Filtrar el DataFrame original para quedarnos solo con esas 10
            df_filtered = df[df[col].isin(top_10_categories)]
            
            plt.figure(figsize=(12, 6))
            
            # 3. Usar countplot es mucho más directo para categórica vs categórica
            # x es el target (0, 1) y hue es la variable con muchas clases
            ax = sns.countplot(data=df_filtered, x=cat_col1, hue=col)
            
            if col in ['description', 'country']:
                plt.title(f'Top 10 de {col} por {cat_col1}')
                plt.xlabel(f'{cat_col1}')
                plt.ylabel('Conteo')
            
            else:
                plt.title(f'Relación entre {col} y {cat_col1}')
                plt.xlabel(f'{cat_col1}')
                plt.ylabel('Conteo')
            
            # 4. Ajustar la leyenda para que no tape el gráfico
            plt.legend(title=col, bbox_to_anchor=(1.05, 1), loc='upper left')

            # 5. Mostrar valores sobre las barras (Usando bar_label que es más limpio)
            for container in ax.containers:
                ax.bar_label(container, padding=3)

            plt.tight_layout()
            plt.show()

#####################################################################################################

def temporal_rv_trans(df:pd.DataFrame) -> None:

    """
        Visualiza la evolución temporal del Revenue y el número de transacciones 
        en un gráfico de doble eje Y, destacando un periodo de corte.

        La función agrupa los datos por mes, calcula el ingreso total y el conteo 
        de transacciones únicas, y genera una comparativa visual que incluye una 
        zona sombreada para identificar el periodo de validación.

        Parameters
        ----------
        df : pandas.DataFrame
            El DataFrame de entrada. Debe contener las columnas 'invoicedate' (datetime), 
            'revenue' (numérica) e 'invoice' (identificador de transacción).

        Returns
        -------
        None
            Despliega un gráfico de líneas con doble eje Y mediante plt.show().
        """

    df['year_month'] = df['invoicedate'].dt.to_period('M')

    temporal = df.groupby('year_month').agg(
        revenue       =('revenue', 'sum'),
        n_transacciones=('invoice', 'nunique')
    ).reset_index()

    temporal['year_month_dt'] = temporal['year_month'].dt.to_timestamp()

    # Línea de corte temporal
    fecha_corte = df['invoicedate'].max() - pd.DateOffset(months=3)

    # Gráfico con doble eje Y
    fig, ax1 = plt.subplots(figsize=(14, 5))

    # Eje izquierdo → Revenue
    color_rev = '#2980B9'
    ax1.plot(temporal['year_month_dt'], temporal['revenue'], 
            color=color_rev, linewidth=2, marker='o', markersize=4,
            label='Revenue')
    ax1.set_xlabel('Mes')
    ax1.set_ylabel('Revenue', color=color_rev)
    ax1.tick_params(axis='y', labelcolor=color_rev)
    ax1.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{x/1000:.0f}k')
    )

    # Eje derecho → Nº transacciones
    ax2 = ax1.twinx()
    color_tx = '#E67E22'
    ax2.plot(temporal['year_month_dt'], temporal['n_transacciones'],
            color=color_tx, linewidth=2, marker='s', markersize=4,
            linestyle='--', label='Nº Transacciones')
    ax2.set_ylabel('Nº Transacciones', color=color_tx)
    ax2.tick_params(axis='y', labelcolor=color_tx)

    # Línea de corte temporal
    ax1.axvline(x=fecha_corte, color='red', linestyle='--', 
                linewidth=1.5, label=f'Corte temporal ({fecha_corte.strftime("%b %Y")})')
    ax1.axvspan(fecha_corte, temporal['year_month_dt'].max(), 
                alpha=0.08, color='red', label='Período validación')

    # Leyenda unificada de ambos ejes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    ax1.set_title('Evolución mensual de Revenue y Transacciones', 
                fontweight='bold', fontsize=13)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#####################################################################################################

def plot_distribution_target(y_train:pd.Series, y_test:pd.Series) -> None:
    """
    Compara visualmente la distribución de la variable objetivo entre los 
    conjuntos de entrenamiento (Train) y prueba (Test).

    La función genera dos gráficos de barras paralelos que muestran el conteo 
    absoluto de cada clase, incluyendo etiquetas de porcentaje sobre cada barra 
    para verificar que el split sea balanceado y representativo.

    Parameters
    ----------
    y_train : pandas.Series
        Etiquetas del conjunto de entrenamiento.
    y_test : pandas.Series
        Etiquetas del conjunto de prueba.

    Returns
    -------
    None
        Muestra la comparativa visual mediante plt.show().
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    for ax, (split_name, y_split) in zip(axes, [('Train', y_train), ('Test', y_test)]):
        counts = y_split.value_counts()
        bars = ax.bar(['No repite', 'Sí repite'], counts.values,
                    color=['#E07B7B', '#7BA7E0'], edgecolor='white', linewidth=0.8)
        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                    f'{val/len(y_split)*100:.1f}%',
                    ha='center', va='bottom', fontsize=10)
        ax.set_title(f'Distribución Target - {split_name}', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nº de clientes')
        ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.show()

#####################################################################################################

def plot_log(cols_log:list, X_train:pd.DataFrame):
    """
    Compara visualmente la distribución original de una lista de variables 
    frente a su transformación logarítmica (log1p).

    La función genera una matriz de histogramas donde la primera fila muestra 
    las variables originales y la segunda fila muestra las variables tras aplicar 
    `log(1 + x)`. Incluye el cálculo del coeficiente de asimetría (skewness) 
    para evaluar el impacto de la transformación.

    Parameters
    ----------
    cols_log : list of str
        Lista con los nombres de las columnas que se desean transformar y visualizar.
    X_train : pandas.DataFrame
        El DataFrame que contiene las variables originales.

    Returns
    -------
    None
        Despliega la figura con los histogramas comparativos mediante plt.show().
    """
    fig, axes = plt.subplots(2, 4, figsize=(16, 7))

    for i, col in enumerate(cols_log):
        # Original
        axes[0, i].hist(X_train[col], bins=50, color='#7BA7E0', edgecolor='white')
        axes[0, i].set_title(f'{col}\n(original)', fontsize=10, fontweight='bold')
        axes[0, i].set_ylabel('Frecuencia' if i == 0 else '')
        skew_orig = X_train[col].skew()
        axes[0, i].text(0.97, 0.95, f'skew={skew_orig:.2f}', transform=axes[0, i].transAxes,
                        ha='right', va='top', fontsize=9, color='#333')

        # Transformada
        transformed = np.log1p(X_train[col])
        axes[1, i].hist(transformed, bins=50, color='#7BC98E', edgecolor='white')
        axes[1, i].set_title(f'log1p({col})', fontsize=10, fontweight='bold')
        axes[1, i].set_ylabel('Frecuencia' if i == 0 else '')
        skew_log = transformed.skew()
        axes[1, i].text(0.97, 0.95, f'skew={skew_log:.2f}', transform=axes[1, i].transAxes,
                        ha='right', va='top', fontsize=9, color='#333')

    for ax in axes.flat:
        ax.spines[['top', 'right']].set_visible(False)

    fig.suptitle('Efecto de la transformación log1p en variables asimétricas', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()

#####################################################################################################

def ROC_Curve_CM(y_test: np.array, predictions: np.array, auc_test: float,
              model_name: str = 'Modelo', y_pred: np.array = None) -> None:
    """
    Genera un panel de evaluación que incluye la curva ROC y, opcionalmente, 
    la matriz de confusión para un modelo de clasificación binaria.

    Esta visualización permite analizar la capacidad de discriminación del modelo 
    (AUC) y su precisión por clase (Matriz de Confusión) en una sola figura 
    comparativa.

    Parameters
    ----------
    y_test : numpy.ndarray
        Etiquetas reales del conjunto de prueba (0 o 1).
    predictions : numpy.ndarray
        Probabilidades estimadas de la clase positiva (obtenidas con `predict_proba`).
    auc_test : float
        Valor del área bajo la curva ROC (AUC) calculado previamente.
    model_name : str, optional
        Nombre del modelo para mostrar en la leyenda (ej. 'Random Forest'). 
        Por defecto es 'Modelo'.
    y_pred : numpy.ndarray, optional
        Etiquetas predichas (0 o 1) tras aplicar un umbral de decisión. 
        Si se proporciona, se graficará la matriz de confusión a la derecha. 
        Por defecto es None.

    Returns
    -------
    None
        La función despliega los gráficos mediante plt.show().
    """
    show_cm = y_pred is not None
    ncols   = 2 if show_cm else 1
    fig, axes = plt.subplots(1, ncols, figsize=(13 if show_cm else 7, 5))

    # Si solo hay un subplot, axes no es lista → lo normalizamos
    ax_roc = axes[0] if show_cm else axes

    # Curva ROC
    fpr, tpr, _ = roc_curve(y_test, predictions)

    ax_roc.plot(fpr, tpr, color='#3A86FF', linewidth=2,
                label=f'{model_name} (AUC = {auc_test:.2f})')
    ax_roc.plot([0, 1], [0, 1], 'k--', linewidth=0.8, label='Random Guess')
    ax_roc.fill_between(fpr, tpr, alpha=0.08, color='#3A86FF')

    ax_roc.set_xlabel('False Positive Rate', fontsize=11)
    ax_roc.set_ylabel('True Positive Rate', fontsize=11)
    ax_roc.set_title('Curva ROC', fontsize=12, fontweight='bold')
    ax_roc.legend(fontsize=10)
    ax_roc.spines[['top', 'right']].set_visible(False)

    # Matriz de confusión 
    if show_cm:
        ConfusionMatrixDisplay.from_predictions(
            y_test, y_pred,
            display_labels=['No repite', 'Sí repite'],
            ax=axes[1],
            colorbar=False,
            cmap='Blues'
        )
        axes[1].set_title('Matriz de Confusión', fontsize=12, fontweight='bold')
        axes[1].grid(False)   # elimina las cuadrículas internas

    plt.tight_layout()
    plt.show()

#####################################################################################################

def plot_features_importance(fitted_model, fitted_prep, BEST_MODEL_NAME):
    """
    Extrae, limpia y visualiza la importancia de las variables (features) 
    utilizadas por el modelo entrenado.

    La función identifica automáticamente si el modelo utiliza importancias por 
    ganancia (árboles) o coeficientes (modelos lineales), recupera los nombres 
    de las variables procesadas por el preprocesador y genera un gráfico de 
    barras horizontales ordenado.

    Parameters
    ----------
    fitted_model : estimator
        El modelo de Scikit-Learn ya entrenado (ej. RandomForest, LogisticRegression).
    fitted_prep : ColumnTransformer
        El preprocesador ya ajustado que contiene el método `get_feature_names_out`.
    BEST_MODEL_NAME : str
        Nombre descriptivo del modelo para incluir en el título del gráfico.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame con las columnas 'Feature' e 'Importance', ordenado de 
        mayor a menor relevancia.
    """
    # Recuperar nombres de features tras el ColumnTransformer
    feature_names_out = fitted_prep.get_feature_names_out()
    # Limpiar prefijos del ColumnTransformer (e.g. 'log_scale__frequency' → 'frequency')
    feature_names_clean = [name.split('__')[-1] for name in feature_names_out]

    # Extraer importancias según el tipo de modelo
    if hasattr(fitted_model, 'feature_importances_'):
        importances = fitted_model.feature_importances_
        imp_type = 'Importancia (Gain)'
    elif hasattr(fitted_model, 'coef_'):
        importances = np.abs(fitted_model.coef_[0])
        imp_type = 'Coeficiente'
    else:
        raise ValueError('El modelo no expone feature_importances_ ni coef_')

    df_importance = pd.DataFrame({
        'Feature':    feature_names_clean,
        'Importance': importances
    }).sort_values('Importance', ascending=False).reset_index(drop=True)

    # Gráfica
    fig, ax = plt.subplots(figsize=(9, 5))

    palette = sns.color_palette('Blues_r', len(df_importance))
    bars = ax.barh(df_importance['Feature'][::-1],
                df_importance['Importance'][::-1],
                color=palette, edgecolor='white')

    for bar, val in zip(bars, df_importance['Importance'][::-1]):
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontsize=9)

    ax.set_xlabel(imp_type, fontsize=11)
    ax.set_title(f'Feature Importance - {BEST_MODEL_NAME}', fontsize=12, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.show()

    return df_importance