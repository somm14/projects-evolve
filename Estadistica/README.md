# **Modelado Estadístico – Regresión y Comparación de Modelos**

*Mini proyecto – Máster en Data Science & IA*

---

## **Descripción del proyecto**

Este repositorio contiene el desarrollo de un análisis estadístico aplicado a modelado predictivo mediante técnicas de regresión, así como el análisis de series temporales

Forma parte de la evaluación del máster y busca reforzar los fundamentos matemáticos y prácticos del modelado estadístico.

## **Objetivos del proyecto**

- Comprender el funcionamiento matemático de la regresión lineal y logística.
- Analizar la relación entre variables predictoras y variable objetivo.
- Evaluar la capacidad predictiva del modelo mediante métricas estadísticas.
- Comparar implementación manual vs implementación optimizada (sklearn).
- Analizar la convergencia del modelo y posibles limitaciones.
- Analizar tendencias y estacionalidad en una serie temporal generada.
  
## **Dataset utilizado**

- Fuente: [Kaggle – Yellow Taxi Trip records for Jan-Dec 2025](https://www.kaggle.com/datasets/aryanpatel212/cleaned-nyc-taxi-trip-data-2025-sample)

Debido al gran tamaño del dataset original, se extrajo una muestra de 50.000 registros para poder trabajar de forma eficiente, por lo que el archivo `.csv` original no está incluido en el repositorio por su tamaño.

Este dataset se utilizó en las Partes 1 y 2 del proyecto, centradas en análisis estadístico y modelado inicial.

## 📁 **Estructura del repositorio**
├── data/  
│   ├── data_dictionary_trip_records_yellow.pdf  
│   ├── Sample_NYC_Taxi_Analysis.csv  
│   └── taxi_zone_lookup.csv  
│  
├── html/  
│   ├── 01_Sample.html  
│   └── PracticaEstadistica__Malpica_Soraya_.html  
│  
├── utils/  
│   ├── clean_pipeline.py  
│   ├── graphs_pipeline.py  
│   └── utils_general.py  
│  
├── 01_Sample.ipynb  
├── PracticaEstadistica__Malpica_Soraya_.ipynb  
└── README.md  

## 👩‍💻 **Autoría**

Proyecto realizado como parte del Máster en Data Science & IA, por *Soraya Malpica Montes*.
