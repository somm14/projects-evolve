# **Predicción de Tasa de Recompra de Clientes**

*Mini proyecto del Máster en Data Science & IA*

---

## **Descripción del proyecto**

Este repositorio contiene un proyecto de Machine Learning de extremo a extremo enfocado en la fidelización de 
clientes. 

El **objetivo** es predecir la probabilidad de que un cliente realice una nueva compra tras un periodo de 
observación, permitiendo a la empresa de e-commerce anticiparse al abandono (churn) y optimizar sus presupuestos 
de marketing.

A diferencia de modelos convencionales, este proyecto implementa un umbral de decisión personalizado para maximizar
el AUC, garantizando que la estrategia de negocio capture a la gran mayoría de clientes con potencial de recompra.

## 📁 **Estructura del repositorio**  
├── data/  
|   ├── raw/  
|       └── online_retail_II.xlsx          # +500k registros originales  
|   └── clean/  
|       ├── online_retail_clean_all.csv    # Dataset limpio con todos los registros originales  
|       └── online_retail_unique.csv       # Dataset procesado (5,281 clientes)  
├── utils/  
|   ├── utils_description.py               # Script de funciones para el análisis descriptivo  
|   ├── utils_hipotesis.py                 # Script de funciones para el contraste de hipótesis  
|   ├── utils_preprocessing.py             # Script de funciones para el preprocesamiento  
|   ├── utils_train.py                     # Script de funciones para el entrenamiento  
|   └── utils_visualization.py             # Script de funciones para visualizaciones gráficas  
├── 01_Tratamiento_datos.ipynb    
├── 02_EDA.ipynb   
├── 03_Modelización_y_Optuna.ipynb  
├── 03_Preprocesamiento_y_Modelado.ipynb  
├── README.md  
└── requirements.txt

## 📦 **Dataset utilizado**

Los datos fueron proporcionados por el profesor encargado del módulo de Machine Learning.

## **Pipeline de Datos**

1. **Limpieza**: Procesamiento de más de 500k registros, eliminación de cancelaciones (devoluciones), tratamiento de valores nulos en IDs de cliente y filtrado de ruido transaccional.
2. **Transformación RFM**: Agregación de datos a nivel de cliente único ($n=5,281$) calculando métricas de:
     - `recency`: Días desde la última compra.
     - `frequency`: Número total de pedidos.
     - `monetary`: Valor total gastado.
     - Variables derivadas: Media de días entre pedidos, tasa de cancelación, etc.

## **Resultados del Modelo**
Se compararon tres algoritmos: **Logistic Regression** (como baseline), **Random Forest** y **LightGBM**. La optimización de hiperparámetros se realizó mediante Optuna.

Tras la optimización se consiguió un AUC en el conjunto de test de un 0.81 con el modelo **LightGBM**.

## **Explicabilidad (DALEX)**

Utilizando la librería **DALEX**, se extrajeron insights críticos para entender el comportamiento del consumidor:
- **Variable principal**: La variable `recency` es el predictor más fuerte (impacto de $+0.107$ en el modelo).
- **Puntos de fuga (PDP)**: La probabilidad de recompra cae drásticamente después de los 120 días de inactividad y se estanca por completo a los 370 días.
- **Curva de madurez**: La fidelidad del cliente se estabiliza significativamente a partir de los 15 pedidos realizados.
- **Correlación de riesgo**: Se validó una correlación de $r = 0.82$ entre `recency` y `avg_days_between_orders`, confirmando que el retraso en el patrón habitual de compra es el mejor indicador de abandono.

## **Conclusiones y Estrategia de Negocio**
  
A partir del modelo, se proponen tres ejes de actuación:

1. **Prevención activa**: Lanzar campañas de reactivación automáticas (cupones, recordatorios) antes de alcanzar los 120 días de inactividad.
2. **Programa VIP**: Segmentar y proteger a clientes con más de 15 pedidos, ya que presentan una inercia de compra superior.
3. **Eficiencia de gasto**: Cesar la inversión publicitaria y el envío de catálogos a clientes con más de 370 días sin actividad, dado que la probabilidad de conversión es marginal.

## **Autoría**
Proyecto realizado por *Soraya Malpica Montes* como parte del Máster en Data Science & IA.
