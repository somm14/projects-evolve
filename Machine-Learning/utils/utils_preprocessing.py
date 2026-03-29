import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, FunctionTransformer

def build_preprocessor(feature_list:list, cols_log_transform:list) -> ColumnTransformer:
    """
    Configura y devuelve un objeto ColumnTransformer para automatizar el preprocesamiento 
    de variables numéricas.

    La función separa las características en dos grupos: aquellas que requieren una 
    transformación logarítmica previa al escalado y aquellas que solo requieren 
    escalado estándar. Utiliza un Pipeline para encadenar las operaciones de 
    logaritmo y estandarización cuando sea necesario.

    Parameters
    ----------
    feature_list : list of str
        Lista completa de nombres de las columnas que se utilizarán como predictores 
        (features) en el modelo.
    cols_log_transform : list of str
        Subconjunto de columnas de `feature_list` a las que se les debe aplicar 
        la transformación logarítmica `log(1 + x)`.

    Returns
    -------
    sklearn.compose.ColumnTransformer
        Un transformador listo para ser ajustado (`fit`) y aplicado (`transform`) 
        que procesa las columnas en paralelo y descarta las no especificadas.
    """
    log_cols   = [c for c in cols_log_transform if c in feature_list]
    other_cols = [c for c in feature_list if c not in cols_log_transform]

    transformers = []
    if log_cols:
        transformers.append((
            'log_scale',
            Pipeline([
                ('log',   FunctionTransformer(np.log1p, validate=True, feature_names_out='one-to-one')),
                ('scale', StandardScaler())
            ]),
            log_cols
        ))
    if other_cols:
        transformers.append((
            'scale',
            StandardScaler(),
            other_cols
        ))

    return ColumnTransformer(transformers=transformers, remainder='drop')


