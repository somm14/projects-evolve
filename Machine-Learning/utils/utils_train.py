
import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_auc_score

from lightgbm import LGBMClassifier

def cv_evaluate(X:pd.DataFrame, y, dict_modelos:dict, configs_prepro:list, scoring_list:list = None) -> pd.DataFrame:
    """
    Realiza una evaluación exhaustiva de múltiples modelos y configuraciones de variables mediante validación cruzada estratificada.

    La función itera sobre un diccionario de modelos y una lista de configuraciones de preprocesamiento, construyendo pipelines dinámicos 
    y calculando métricas de rendimiento promedio para cada combinación.

    Parameters
    ----------
    X : pandas.DataFrame
        El conjunto de datos con todas las características (features).
    y : array-like
        La variable objetivo (target).
    dict_modelos : dict
        Diccionario donde las llaves son nombres de modelos (str) y los valores son instancias de estimadores de Scikit-Learn.
    configs_prepro : list of tuples
        Lista de configuraciones en formato: `(nombre_set, objeto_preprocesador, lista_columnas)`.
    scoring_list : list of str, optional
        Lista de métricas de Scikit-Learn a evaluar (ej. ['roc_auc', 'f1']). 
        Si es None, usa ['roc_auc', 'f1', 'precision', 'recall'].

    Returns
    -------
    pandas.DataFrame
        Un DataFrame resumen ordenado por ROC_AUC de forma descendente, conteniendo el rendimiento promedio de cada métrica por experimento.
    """
    if scoring_list is None:
        scoring_list = ['roc_auc', 'f1', 'precision', 'recall']
        
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = []

    for model_name, model in dict_modelos.items():
        for feat_set_name, preprocessor, feats in configs_prepro:
            
            # Construcción del Pipeline
            pipe = Pipeline([
                ('preprocessor', clone(preprocessor)),
                ('model', clone(model))
            ])
            
            # Validación Cruzada
            cv_results = cross_validate(
                pipe, X[feats], y,
                cv=cv, 
                scoring=scoring_list, 
                n_jobs=-1
            )
            
            # Extracción de métricas
            res_dict = {
                'Modelo': model_name,
                'Features': feat_set_name
            }
            
            for metric in scoring_list:
                # Mapeo de nombre de métrica a clave de cv_results (test_nombre)
                res_dict[metric.upper()] = cv_results[f'test_{metric}'].mean()
                
            results.append(res_dict)
            print(f"{model_name:<22} [{feat_set_name:<8}] AUC: {res_dict['ROC_AUC']:.4f}")

    # Creación y ordenación del DataFrame
    df_results = pd.DataFrame(results).sort_values('ROC_AUC', ascending=False).reset_index(drop=True)
    return df_results

#####################################################################################################

def objective(trial, x_train:pd.DataFrame, y_train:pd.Series, best_preprocessor:ColumnTransformer, best_feats:list, model_class) -> float:
    """
    Función objetivo para la optimización de hiperparámetros mediante Optuna.

    Define el espacio de búsqueda de parámetros para diferentes algoritmos de 
    clasificación (Logistic Regression, Random Forest o LightGBM) y evalúa 
    cada combinación (trial) mediante validación cruzada para maximizar el ROC-AUC.

    Parameters
    ----------
    trial : optuna.trial.Trial
        Un objeto que representa un proceso de optimización individual y permite 
        sugerir valores para los hiperparámetros.
    x_train : pandas.DataFrame
        Conjunto de datos de entrenamiento con las características.
    y_train : array-like
        Etiquetas reales para el entrenamiento.
    best_preprocessor : sklearn.compose.ColumnTransformer
        El preprocesador ya configurado que se integrará en el Pipeline.
    best_feats : list of str
        Lista de nombres de las columnas seleccionadas para el modelo.
    model_class : type
        La clase del modelo a optimizar (LogisticRegression, 
        RandomForestClassifier o LGBMClassifier).

    Returns
    -------
    float
        La media del score ROC-AUC obtenido a través de las 5 particiones de 
        la validación cruzada.
    """
    if model_class == LogisticRegression:
        C        = trial.suggest_float('C', 1e-3, 10.0, log=True)
        penalty  = trial.suggest_categorical('penalty', ['l1', 'l2'])
        cw       = trial.suggest_categorical('class_weight', [None, 'balanced'])
        solver   = 'liblinear' if penalty == 'l1' else 'lbfgs'

        model = model_class(
            C=C, penalty=penalty, solver=solver,
            class_weight=cw, max_iter=1000, random_state=42
        )
    
    elif model_class == RandomForestClassifier:
        n_est      = trial.suggest_int('n_estimators', 100, 600)
        max_depth  = trial.suggest_int('max_depth', 3, 20)
        min_leaf   = trial.suggest_int('min_samples_leaf', 1, 20)
        max_feat   = trial.suggest_categorical('max_features', ['sqrt', 'log2', 0.5])
        cw         = trial.suggest_categorical('class_weight', [None, 'balanced'])

        model = model_class(
            n_estimators=n_est, max_depth=max_depth,
            min_samples_leaf=min_leaf, max_features=max_feat,
            class_weight=cw, random_state=42, n_jobs=-1
        )
    elif model_class == LGBMClassifier:
        n_est        = trial.suggest_int('n_estimators', 100, 600)
        lr_rate      = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)
        max_depth    = trial.suggest_int('max_depth', 3, 12)
        num_leaves   = trial.suggest_int('num_leaves', 20, 150)
        min_child    = trial.suggest_int('min_child_samples', 10, 100)
        cw           = trial.suggest_categorical('class_weight', [None, 'balanced'])

        model = model_class(
            n_estimators=n_est, learning_rate=lr_rate,
            max_depth=max_depth, num_leaves=num_leaves,
            min_child_samples=min_child, class_weight=cw,
            random_state=42, verbose=-1, n_jobs=-1
        )
    
    else:
        print('Solo se puede meter estos modelos - (LogisticRegression, RandomForestClassifier, LGBMClassifier)')

    pipe = Pipeline([('preprocessor', clone(best_preprocessor)),
                    ('model', model)])
    cv_inner = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_validate(pipe, x_train[best_feats], y_train,
                            cv=cv_inner, scoring='roc_auc', n_jobs=-1)
    return scores['test_score'].mean()

#####################################################################################################