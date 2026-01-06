# **EDA de Hábitos y Salud – BRFSS 2022**

*Mini proyecto del Máster en Data Science & IA*

---

## **Descripción del proyecto**

Este repositorio contiene un *Análisis Exploratorio de Datos (EDA)* basado en una selección de variables del dataset **Behavioral Risk Factor Surveillance System 2022 (BRFSS)**, una base de datos pública elaborada por los CDC (Centers for Disease Control and Prevention). El dataset incluye información real sobre hábitos de salud, bienestar físico y mental, ejercicio, sueño, nutrición y factores sociodemográficos.

Este proyecto forma parte de la evaluación del máster y tiene como objetivo practicar un flujo completo de EDA: carga, exploración, limpieza y visualización básica.

## **Objetivos del análisis**

- Examinar la estructura del dataset y evaluar la calidad de los datos.

- Identificar problemas comunes: valores nulos, inconsistencias, duplicados y codificaciones irregulares.

- Realizar un proceso de limpieza justificado.

- Crear visualizaciones básicas que permitan comprender las características principales del dataset.

- Documentar el proceso de forma clara y ordenada.

## 📁 **Estructura del repositorio**
├── data/  
│   ├── LLCP2022.XPT               # Archivo original  
│   ├── USCODE22_LLCP_102523.HTML  # Archivo donde se encuentra la información de las variables codificadas  
│   ├── data_clean.csv             # Dataset limpio  
│   ├── data_rename.csv            # Dataset descodificada y los nombres de las columnas cambiadas  
│   └── mapped_data.csv            # Dataset mapeado  
├── notebooks/  
│   ├── 00_Introduccion_y_estrategia.ipynb  
│   ├── 01_Mapeo_descodificacion.ipynb  
│   ├── 02_Primer_analisis_descriptivo.ipynb  
│   ├── 03_Limpieza_y_preparacion.ipynb  
│   ├── 04_Visualizaciones_y_analisis.ipynb  
│   └── 05_Conclusiones.ipynb  
├── scripts  
│   ├── cleaning.py  
│   ├── individual_visualization.py  
│   ├── mapping.py  
│   ├── relationship_visualization.py  
│   └── variables.py  
├── README.md  
└── requirements.txt                 

## 📦 **Dataset utilizado**

- Fuente: CDC – Behavioral Risk Factor Surveillance System (BRFSS)

- Año: 2022

- Tipo de datos: encuesta telefónica, datos individuales

- Enlace oficial: https://www.cdc.gov/brfss/annual_data/2022

El dataset original cuenta con cientos de variables; para este proyecto se ha realizado una selección enfocada en hábitos de vida, salud mental, salud física y variables sociodemográficas.

## 🛠 **Proceso de trabajo**

### Carga de datos:
Se realizó un mapeo y una descodificación de los datos ya que su origen eran de tipo numérico.

### Exploración inicial:
Se visualizó cada una de las variables seleccionadas para analizar con más profundidad la distribución y, así, tomar decisiones correctas ante la limpieza.

### Limpieza de datos:
- Se eliminó aquella columna con un porcentaje de nulos mayor del 90% por falta de información.
- Se categorizaron algunos valores pertinentes y se convirtió otras a tipo numérico.
- Se decidió no imputar valores nulos para no perder información o sesgarla.
  
### Visualizaciones básicas:
- Se utilizó **gráficas de barras** para analizar variables categóricas
- Se hizo uso de **BoxPlot** para realizacionar variables numéricas con categóricas.
- **Heatmap** para realizar análisis trivariante.
- Librería `folium` para visualizar los diferentes estados de EEUU.

## 🧠 **Conclusiones**
1. Hábitos de vida
- **Ejercicio** -> Es el factor más protector del estudio. Una persona diabética activa tiene menos días de mala salud que una persona sana sedentaria.

- **Sedentarismo + Enfermedad** (especialmente Diabetes) -> La peor combinación posible.

- **Tabaco** ->  El hábito más dañino: afecta más a la salud mental que el propio cáncer. Fumar duplica los días de malestar mental.

- **Alcohol** -> Los abstemios muestran peor salud debido a la "paradoja del abstemio enfermo" (muchos dejan de beber por enfermedad). El mejor perfil es el consumo moderado, aunque ¿realmente es mejor a largo plazo?

2. Factores biológicos

- **IMC** -> Es uno de los predictores más fuertes en diabetes, asma y enfermedades cardiovasculares.

- **Cáncer** -> No muestra una relación clara con el IMC en esta muestra.

3. Salud mental

- Enfermedades como diabetes y cardiopatías duplican los días de mala salud mental.

- Cáncer no empeora significativamente la salud mental (indica resiliencia).

- El peor perfil mental corresponde a personas con síntomas o diagnósticos inciertos (“NS/NC”).

4. Condición socioeconómica

- **Ingresos y educación** funcionan como factores protectores.

- Estar “incapacitado de trabajar” es el mayor predictor individual de mala salud.

- Los mayores de 65 años presentan mejor salud mental que los jóvenes.

5. Geografía

- El Sur y la región de los Apalaches concentran los peores indicadores de salud física y mental.

- Estas zonas coinciden con menores recursos, reforzando el vínculo entre territorio, economía y salud.

## 👩‍💻 **Autoría**

Proyecto realizado como parte del Máster en Data Science & IA, por *Soraya Malpica Montes*.
