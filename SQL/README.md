# **Proyecto SQL: Análisis sobre la adaptabilidad en la Educación Online**

*Mini proyecto del Máster en Data Science & IA*

---

## **Descripción del proyecto**

Este repositorio contiene un proyecto completo que combina diseño de base de **datos relacional, carga y transformación de datos, consultas SQL y Análisis Exploratorio de Datos (EDA)** a partir de un dataset sobre uso de Internet, nivel educativo y variables sociodemográficas.

El objetivo principal del proyecto es **simular un flujo de trabajo realista desde cero**, comenzando por la creación del esquema de la base de datos, la importación de datos en crudo y, posteriormente, el análisis exploratorio y relacional de la información.

El proyecto está pensado para demostrar competencias en:

- Diseño de bases de datos relacionales
- SQL (joins, vistas, agregaciones)
- Análisis bivariado y multivariado
- Documentación clara y reproducible

## **Objetivos del análisis**

- Diseñar y crear una base de datos relacional coherente a partir de datos en crudo.
- Cargar y estructurar los datos respetando relaciones y claves.
- Explorar la relación entre la adaptabilidad de la educación online y el uso de Internet, edad, factores socioeconómicos y sociodemográficos.
- Analizar patrones de comportamiento digital según el contexto social.
- Practicar un flujo completo de análisis orientado a datos reales.

## 📁 **Estructura del repositorio**
├── data/  
|    └── students_adaptability_level_online_education  --> Dataset en crudo (importado manualmente)  
├── 01_schema.sql                 --> Creación del esquema y tablas  
├── 02_data.sql                   --> Inserción y transformación de datos  
├── 03_eda.sql                    --> Consultas SQL y realización del EDA 
├── 04_model.png                 --> Modelo relacional de la base de datos
└── Presentación.pdf            --> Slides de presentación


## **Flujo de trabajo (paso a paso)**  

1️⃣ **Creación de la base de datos**

El proyecto comienza desde cero, creando la estructura de la base de datos relacional.

- Ejecutar el archivo:

``` pgsql
01_schema.sql
```

Este script:

- Crea la base de datos
- Define las tablas
- Establece claves primarias y foráneas
- Garantiza la integridad relacional

📌 En el archivo `04_model.png` se incluye el modelo relacional completo para facilitar la comprensión de la estructura.

2️⃣ **Importación del dataset en crudo**

Antes de ejecutar el siguiente script, es necesario importar manualmente el dataset original en la base de datos.

Pasos:

1. Colocar el archivo CSV original en data/
2. Importar el dataset en la base de datos correspondiente usando la herramienta de gestión de base de datos (pgAdmin, MySQL Workbench, DBeaver, etc.)
3. Verificar que los datos se han cargado correctamente

3️⃣ **Carga de datos**

Una vez importados los datos en crudo, ejecutar:

``` pgsql
02_data.sql
```

Este script se encarga de:

- Insertar los datos a partir del dataset en crudo
- Poblar tablas normalizadas
- Preparar la información para el análisis

4️⃣ **Consultas, vistas SQL y EDA**

El archivo:

``` pgsql
03_eda.sql
```

incluye:

- Consultas bivariadas y multivariadas.
- Agregaciones y agrupaciones.
- Creación de vistas para facilitar el análisis posterior.
- Relaciones entre variables sociodemográficas y socioeconómicas.
- Impacto de estas variables en el desarrollo de la adaptabilidad.

## **Dataset utilizado**

- Tipo de datos: encuesta
- Variables principales:
  - Uso de Internet
  - Tipo de institución
  - Nivel educativo
  - Rango de edad
  - Nivel financiero
  - Nivel de adaptación -> **Target**
- Fuente: [Kaggle](https://www.kaggle.com/datasets/mdmahmudulhasansuzan/students-adaptability-level-in-online-education?resource=download)

El dataset ha sido tratado como datos reales, priorizando la coherencia relacional y la trazabilidad del proceso.

## **Conclusiones**

El análisis permite identificar:

- Patrones claros entre nivel educativo y tipo de acceso a Internet.
- Diferencias significativas en el uso digital según la edad y el entorno.
- El papel del contexto socioeconómico como factor condicionante del acceso tecnológico.
- La importancia de una correcta estructuración de datos para realizar análisis fiables.

## 👩‍💻 **Autoría**

Proyecto realizado por *Soraya Malpica Montes* como parte de la formación y portfolio en **Data Science & IA**, con especial énfasis en **SQL y análisis exploratorio**.

