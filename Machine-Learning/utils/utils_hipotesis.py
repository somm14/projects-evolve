import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats



def heatmap_corr(df:pd.DataFrame, var_num:list) -> None:
    """
    Calcula y visualiza la matriz de correlación de Pearson para variables numéricas.

    La función genera un mapa de calor (heatmap) estilizado que permite identificar 
    rápidamente la fuerza y dirección de las relaciones lineales entre las variables 
    seleccionadas.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos.
    var_num : list of str
        Lista de nombres de las columnas numéricas que se incluirán en el 
        análisis de correlación.

    Returns
    -------
    None
        Muestra el gráfico térmico mediante plt.show().
    """
    plt.style.use('ggplot')
    sns.set_palette('husl')


    fig, ax = plt.subplots(figsize=(10, 7))

    corr_matrix = df[var_num].corr()

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        vmin=-1, vmax=1,
        square=True,
        linewidths=0.5,
        ax=ax
    )

    ax.set_title('Matriz de correlaciones — Features RFM', 
                fontweight='bold', fontsize=13)
    plt.tight_layout()
    plt.show()

#####################################################################################################

def hipo_num_target(df:pd.DataFrame, target:str, var_num:list) -> pd.DataFrame:
    """
    Realiza pruebas de hipótesis no paramétricas para comparar variables numéricas 
    entre dos grupos definidos por una variable objetivo binaria.

    Utiliza la prueba U de Mann-Whitney para determinar si existen diferencias 
    significativas en la distribución de las variables numéricas entre el 
    grupo 0 y el grupo 1 del target.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos.
    target : str
        Nombre de la columna binaria (0 o 1) que define los dos grupos a comparar.
    var_num : list of str
        Lista de nombres de las columnas numéricas que se desean testear.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame resumen ordenado por p-valor que contiene:
        - 'Feature': Nombre de la variable analizada.
        - 'Estadístico U': El valor calculado de la prueba Mann-Whitney.
        - 'p-valor': El nivel de significancia estadística.
        - 'Significativa': Etiqueta visual ('Sí ✅' / 'No ❌') basada en alpha = 0.05.
    """
    grupo_0 = df[df[target] == 0]
    grupo_1 = df[df[target] == 1]

    resultados_num = []

    for feature in var_num:
        stat, p_value = stats.mannwhitneyu(
            grupo_0[feature], 
            grupo_1[feature], 
            alternative='two-sided'
        )
        resultados_num.append({
            'Feature': feature,
            'Estadístico U': round(stat, 2),
            'p-valor': p_value,
            'Significativa': 'Sí ✅' if p_value < 0.05 else 'No ❌'
        })

    df_resultados_num = pd.DataFrame(resultados_num).sort_values('p-valor')
    return df_resultados_num

#####################################################################################################

def hipo_cat_target(df:pd.DataFrame, target:str, var_cat:list) -> pd.DataFrame:
    """
    Realiza pruebas de independencia Chi-cuadrado de Pearson para evaluar la 
    relación entre variables categóricas y una variable objetivo.

    La función procesa una lista de variables, aplicando un tratamiento especial 
    a la columna 'country' (agrupando categorías minoritarias) y calcula si 
    existe una asociación estadísticamente significativa con el target.

    Parameters
    ----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos de estudio.
    target : str
        El nombre de la columna que actúa como variable dependiente (objetivo).
    var_cat : list of str
        Lista de nombres de las columnas categóricas que se desean testear.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame resumen que incluye:
        - 'Feature': La variable analizada (incluyendo 'country_mode').
        - 'Chi²': El estadístico de la prueba Chi-cuadrado.
        - 'p-valor': El nivel de significancia obtenido.
        - 'Grados libertad': Los grados de libertad de la tabla de contingencia.
        - 'Significativa': Indicador visual ('Sí ✅' / 'No ❌') basado en alpha = 0.05.
    """
    top_paises = df['country'].value_counts().nlargest(10).index
    df['country_mode'] = df['country'].apply(
        lambda x: x if x in top_paises else 'Other'
    )

    cat_df_2 = [col for col in var_cat if col != 'country']
    cat_df_2.append('country_mode')
    resultados_cat = []

    for feature in cat_df_2:
        tabla = pd.crosstab(df[feature], df[target])
        chi2, p_value, dof, _ = stats.chi2_contingency(tabla)
        resultados_cat.append({
            'Feature'      : feature,
            'Chi²'         : round(chi2, 2),
            'p-valor'      : p_value,
            'Grados libertad': dof,
            'Significativa': 'Sí ✅' if p_value < 0.05 else 'No ❌'
        })

    df_resultados_cat = pd.DataFrame(resultados_cat)
    return df_resultados_cat