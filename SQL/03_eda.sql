USE online_education;

/* 
-----------------------------------------------------------------------
EDA – Análisis Exploratorio de Datos
Proyecto SQL: Adaptabilidad de los estudiantes en la Educación Online
-----------------------------------------------------------------------

--> BLOQUE DE CONTENIDOS:

	1. Origen y naturaleza de los datos
    2. Objetivo del EDA
    3. Creación y carga de dimensiones
    4. Validación de datos
		4.1. Conteo de registros en la tabla de hechos repecto al original
        4.2. Verificación de claves foráneas
		4.3. Comprobación de valores NULL en la tabla de hechos
	5. Análisis univariado
		5.1. Distribución del nivel de adaptabilidad
        5.2. Distribución por género
        5.3. Distribución por rango de edad
        5.4. Nivel educativo
        5.5. Tipo de institución
        5.6. Entorno socioeconómico (localización sintética)
		5.7. Acceso tecnológico
	6. Análisis bivariado
		6.1. Adaptabilidad vs Género
        6.2. Adaptabilidad vs Rango de edad
        6.3. Adaptabilidad vs Nivel educativo
        6.4. Adaptabilidad vs Tipo de institución
		6.5. Adaptabilidad vs Condición financiera
        6.6. Adaptabilidad vs Load Shedding
        6.7. Adaptabilidad vs Acceso tecnológico
        6.8. Adaptabilidad vs Localización (sintética)
	7. Análisis avanzado
		7.1. Ranking comparando la tecnología y la adaptabilidad
        7.2. Ranking de factores socioeconómicos
        7.3. Evolución temporal
        7.4. Proporción de adaptabilidad por ámbito socio económico
	8. Resumen de los datos
    9. Conclusiones
        
    
-----------------------------------------------------------------------
1. ORIGEN Y NATURALEZA DE LOS DATOS

El dataset utilizado proviene de una recopilación pública disponible en Kaggle y ha sido utilizado en distintos estudios académicos 
para analizar la adaptabilidad de estudiantes a la educación online.

Cada registro del dataset representa una observación individual (respuesta), no un estudiante único identificado. Por este motivo, 
el modelo diferencia entre perfiles de estudiante (dimensiones) y observaciones (tabla de hechos).

Muestro, en primer lugar, una visualización de los datos en crudo.
 */
 
SELECT * FROM students_adaptability_level_online_education LIMIT 10;

/* 
El dataset tiene las siguientes columnas:
	- Gender: Tipo de género del estudiante
    - Age: Rang de edad del estudiante
    - Education Level: Nivel de institución educativa
    - Institution Type: Tipo de institución educativa
    - IT Student: Si el estudiante estudia IT o no
    - Location: Si la ubicación del estudiante está en la ciudad
    - Load-shedding: frecuencia de interrupciones eléctricas en la zona del estudiante
    - Financial Condition: Condiciín financiera de la familia
    - Internet Type: Tipo de internet
    - Network Type: Tipo de conexión
    - Class Duration: Duración diaria de la clase.
    - Self Lms: Si el estudiante utiliza una plataforma LMS (Learning Management System) propia o institucional
    - Device: Dispositivo utilizado en clase.
    - Adaptivity Level: Nivel de adaptabilidad
    
-----------------------------------------------------------------------

2. OBJETIVO DEL EDA

Este análisis exploratorio tiene como objetivo extraer insights relevantes sobre la adaptabilidad de los estudiantes a la educación 
online, considerando factores demográficos, institucionales, tecnológicos y socioeconómicos.

Los datos han sido modelados siguiendo un esquema relacional normalizado, separando dimensiones y una tabla de hechos para facilitar el 
análisis y garantizar la integridad de los datos.

-----------------------------------------------------------------------

3. CREACIÓN Y CARGA DE DIMENSIONES

Se crearon varias tablas de dimensión utilizando SELECT DISTINCT para evitar duplicados y asegurar la normalización de los datos.

DIM_STUDENT
Representa perfiles únicos de estudiantes según género, rango de edad y nivel educativo.
 */

SELECT * FROM dim_student;

/*
DIM_INSTITUTION
Contiene información sobre el tipo de institución y si el estudiante pertenece al área IT.
*/

SELECT * FROM DIM_INSTITUTION;

/*
DIM_TECH
Incluye información sobre acceso a internet, tipo de red, dispositivo utilizado y uso de plataformas LMS propias.
*/

SELECT * FROM DIM_TECH;


/*
DIM_LOCALIZATION (dimensión sintética)

El dataset original no especifica información geográfica concreta (país, ciudad). Para enriquecer el análisis socioeconómico, se ha
creado una dimensión de localización sintética que representa distintos entornos territoriales:

- Urban
- Semi-Urban
- Rural

Esta dimensión permite simular análisis por contexto territorial y su posible impacto en la adaptabilidad de los estudiantes.
*/

SELECT * FROM dim_localization;

/*
DIM_SOCIO_ECONOMIC
Recoge información relacionada con la condición financiera, ubicación (sintética) y problemas de suministro eléctrico (load shedding).
En la parte de ubicación (generada sintéticamente) se ha asociado con una coherencia como, por ejemplo, si es urbano lo relaciono con 
mejor infraestructura, si es rural, más problemas.
*/

SELECT * FROM DIM_SOCIO_ECONOMIC;

/*
DIM_CALENDAR (dimensión sintética)

El dataset original no incluye información temporal. Para permitir análisis por año, mes, trimestre y día de la semana, se ha creado
una dimensión de calendario sintética.

Cada registro de la tabla de hechos se asocia a una fecha.
*/

SELECT * FROM dim_calendar;

/*
FACT_ADAPTABILITY

La tabla de hechos contiene todas las observaciones originales del dataset (1000 registros). Cada fila representa una respuesta
individual de un estudiante y se relaciona con las distintas dimensiones mediante claves foráneas.

Esta tabla es el núcleo del análisis exploratorio, ya que permite cruzar información demográfica, institucional, tecnológica,
socioeconómica, geográfica y temporal.
*/

SELECT * FROM FACT_ADAPTABILITY;

/*
-----------------------------------------------------------------------

4. VALIDACIÓN DE DATOS

En este bloque voy a reponder a una pregunta fundamental:

	¿Los datos están completos, bien relacionados y listos para analizar?
*/
-- 4.1. Conteo de registros en la tabla de hechos

SELECT 
	COUNT(DISTINCT fact_id) AS total_registros_fact
FROM fact_adaptability;

SELECT 
	COUNT(*) AS total_registros_original
FROM students_adaptability_level_online_education;

/*
El conteo confirma que la tabla de hechos contiene las 1205 observaciones originales del dataset, garantizando así 
la integridad del proceso de carga.
*/

-- 4.2. Verificación de claves foráneas
-- dim_student
SELECT COUNT(*) AS registros_sin_student
FROM fact_adaptability f
LEFT JOIN dim_student d -- Utilizo el LEFT JOIN para que se muestren los nulos si los hubiera
    ON f.student_id = d.student_id
WHERE d.student_id IS NULL;

-- dim_institution
SELECT COUNT(*) AS registros_sin_institution
FROM fact_adaptability f
LEFT JOIN dim_institution d
    ON f.institution_id = d.institution_id
WHERE d.institution_id IS NULL;

-- dim_tech
SELECT COUNT(*) AS registros_sin_tech
FROM fact_adaptability f
LEFT JOIN dim_tech d
    ON f.tech_id = d.tech_id
WHERE d.tech_id IS NULL;

-- dim_socio_economic (incluye localización sintética)
SELECT COUNT(*) AS registros_sin_socio_economic
FROM fact_adaptability f
LEFT JOIN dim_socio_economic d
    ON f.socio_id = d.socio_id
WHERE d.socio_id IS NULL;

-- dim_calendar
SELECT COUNT(*) AS registros_sin_calendar
FROM fact_adaptability f
LEFT JOIN dim_calendar d
    ON f.calendar_id = d.calendar_id
WHERE d.calendar_id IS NULL;

/*
Durante la validación de claves foráneas se detectó que 205 registros de la tabla de hechos no presentaban correspondencia con la dimensión de 
calendario. Esto se debe a que la dim_calendar fue generada de forma sintética con un rango limitado de fechas (0 a 1000), mientras que la tabla 
de hechos contiene 1205 observaciones. Por lo tanto, se modificó la parte de generación de datos en la tabla 'numbers' añadiendo un elemento más 
para generar números del 0 a 9999 y así cubrir los 1205 registros de la tabla de Hechos.

Esta solución se da ya que el "error" se originaba en una tabla creada sintéticamente. 
Por lo tanto, una vez solventado, no se detectan registros nulos en la tabla de hechos, lo que confirma que todas las claves foráneas 
referencian correctamente a sus respectivas dimensiones.
*/

-- 4.3. Comprobación de valores NULL en la tabla de Hechos.

SELECT
    SUM(CASE WHEN student_id IS NULL THEN 1 ELSE 0 END) AS null_student,
    SUM(CASE WHEN institution_id IS NULL THEN 1 ELSE 0 END) AS null_institution,
    SUM(CASE WHEN tech_id IS NULL THEN 1 ELSE 0 END) AS null_tech,
    SUM(CASE WHEN socio_id IS NULL THEN 1 ELSE 0 END) AS null_socio_economic,
    SUM(CASE WHEN calendar_id IS NULL THEN 1 ELSE 0 END) AS null_calendar,
    SUM(CASE WHEN adaptivity_level IS NULL THEN 1 ELSE 0 END) AS null_adaptivity
FROM fact_adaptability;

/*
La comprobación de valores nulos indica que la tabla de hechos no presenta datos faltantes en sus campos clave ni en la variable objetivo, 
permitiendo un análisis exploratorio fiable.

Tras la validación inicial, se confirma que el modelo de datos es consistente, completo y libre de problemas estructurales. 
Esto permite avanzar con confianza hacia el análisis exploratorio de relaciones entre dimensiones y el nivel de adaptabilidad.

-----------------------------------------------------------------------

5. ANÁLISIS UNIVARIADO

A continuación, analizaré la distribución inicial de las variables con el fin de:
	- Entender la composición del dataset.
	- Detectar posibles desbalances.
    - Establecer una base para el análisis bivariado posterior.
*/

-- 5.1. Distribución del nivel de adaptabilidad

/*
SELECT 
    adaptivity_level,
    COUNT(*) AS total_registros,
    (COUNT(*) * 100.0) / (
		SELECT COUNT(*) FROM fact_adaptability
        ) AS porcentaje
FROM fact_adaptability
GROUP BY adaptivity_level
ORDER BY total_registros DESC; -- Con subconsulta
*/

SELECT 
    adaptivity_level,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje -- Con OVER() me deja usar totales sin perder las filas.
FROM fact_adaptability
GROUP BY adaptivity_level
ORDER BY total_registros DESC;

/*
El nivel de adaptabilidad presenta una distribución no uniforme, lo que sugiere que ciertos perfiles de estudiantes se adaptan mejor que otros 
a la educación online. Esta observación será relevante en análisis posteriores y en posibles enfoques predictivos.
*/

-- 5.2. Distribución por género

SELECT 
    ds.gender,
    COUNT(*) AS total_registros,
	CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_student ds ON f.student_id = ds.student_id
GROUP BY ds.gender
ORDER BY total_registros DESC;

/*
El dataset presenta una distribución de género relativamente equilibrada, por lo que no existen sesgos en el dataset.
*/

-- 5.3. Distribución por rango de edad

-- Creo una vista por si la utilizo posteriormente
DROP VIEW IF EXISTS distripucion_por_edad;
CREATE VIEW distripucion_por_edad AS
SELECT 
    ds.age_range,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_student ds ON f.student_id = ds.student_id
GROUP BY age_range;

SELECT *
FROM DistripucionPorEdad
ORDER BY total_registros DESC;

/*
En esta distribución se puede observar que hay más estudiantes de entre 21 y 25 años que utilizan este tipo de modalidad de estudio, seguido por 
estudiantes entre 11 y 15 años. Además, es importante destacar que las personas entre 26-30 años ocupan el penúltimo puesto con un 5,64%.
También se registran personas con un rango de 1-5 años. Se pueden valorar como outliers ya que a esas edades, ¿es apta la modalidad online?
*/

-- 5.4. Nivel educativo

SELECT 
    ds.education_level,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_student ds ON f.student_id = ds.student_id
GROUP BY ds.education_level
ORDER BY total_registros DESC;

/*
Con esta distribución podemos concluir que la sumatoria de los rangos de edad hace que haya más estudiantes que utilizan este tipo de modalidad 
en edad escolar, siendo los últimos los estudiantes de instituto.
*/

-- Consulto a qué nivel educativo pertenecen cada rango de edad

SELECT 
    age_range,
    education_level
FROM dim_student
GROUP BY age_range, education_level;

/*
Es importante destacar en esta consulta que se puede observar que el rango de 16-20 años se adjudica a los tres niveles educativos.
Con esto podemos reflexionar que los que están en el colegio puede ser porque hayan repetido. Sucede lo mismo con el rango de 21-25 donde
hay una cantidad que están en el instituto.
*/

-- 5.5. Tipo de institución

SELECT 
    di.institution_type,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_institution di ON f.institution_id = di.institution_id
GROUP BY di.institution_type
ORDER BY total_registros DESC;

/*
Se puede observar un dato muy curioso, hay más inntituciones privadas que ofrecen este tipo de modalidad. Además, hay un claro desbalanceo entre 
ambas variables.
*/

-- 5.6. Entorno socioeconómico (localización sintética)

SELECT 
    dl.environment_type AS localizacion,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_localization dl ON f.localization_id = dl.localization_id
GROUP BY dl.environment_type
ORDER BY total_registros DESC;

/*
Teniendo en cuenta que esta información es para simular un análisis por contexto territorial y ,además, se han generado de forma controlada
según varias características, podemos concluir que predomina más los estudiantes que viven en un entorno semi-urbano siendo el porcentaje más
bajo el entorno urbano, posiblemente por la facilidad de recursos.
*/

-- 5.7. Acceso tecnológico

-- Tipo de dispositivo
SELECT 
    dt.device,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_tech dt ON f.tech_id = dt.tech_id
GROUP BY dt.device
ORDER BY total_registros DESC;

/*
Es importante destacar en este análisis que se usa más el móvil que el ordenador, siendo éste más accesible para las usuarios. Además, la 
distribución está muy desbalanceada.
*/

-- Tipo de conexión a internet
SELECT 
    dt.internet_type,
    COUNT(*) AS total_registros,
    CONCAT(ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2), '%') AS porcentaje
FROM fact_adaptability f
JOIN dim_tech dt ON f.tech_id = dt.tech_id
GROUP BY dt.internet_type;

/*
Haciendo relación a la anterior distribución, se confirma el uso de datos del móvil para estudiar de forma online.

-----------------------------------------------------------------------

6. ANÁLISIS BIVARIADO

En este apartadao se analizará la relación entre el nivel de adaptabilidad y distintas variables explicativas (demográficas, 
institucionales, tecnológicas y socioeconómicas), con el fin de identificar factores que influyen en la adaptación a la educación online.
*/

-- 6.1. Adaptabilidad vs Género

SELECT 
    ds.gender,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_student ds 
ON f.student_id = ds.student_id
GROUP BY ds.gender, f.adaptivity_level
ORDER BY ds.gender, total_registros DESC;

/*
El análisis no muestra diferencias significativas entre géneros en términos de adaptabilidad, lo que sugiere que el género no es un 
factor determinante por sí solo.
*/

-- 6.2. Adaptabilidad vs Rango de edad

WITH adaptabilida_por_edad_WT AS
(SELECT
    ds.age_range,

    SUM(CASE WHEN f.adaptivity_level = 'High' THEN 1 ELSE 0 END) AS high_adaptability,
    SUM(CASE WHEN f.adaptivity_level = 'Moderate' THEN 1 ELSE 0 END) AS moderate_adaptability,
    SUM(CASE WHEN f.adaptivity_level = 'Low' THEN 1 ELSE 0 END) AS low_adaptability

FROM fact_adaptability f
JOIN dim_student ds ON f.student_id = ds.student_id
GROUP BY ds.age_range)
SELECT
    d.age_range,
    d.total_registros,
    d.porcentaje,
    a.high_adaptability,
    a.moderate_adaptability,
    a.low_adaptability
FROM distripucion_por_edad d
JOIN adaptabilida_por_edad_WT a ON d.age_range = a.age_range -- Se une por rango de edad ambas vistas
ORDER BY d.total_registros DESC;


/*
En primer lugar, se han separado las agregaciones, por un lado en una vista (distribucion_por_edad) y una CTE para evitar inconsistencias y facilitar el análisis. 

Análisis: 

La mayoría de los estudiantes que pertenecen a rangos de edad comprendido entre los 11–25 años predomina una adaptabilidad moderada a 
la educación online. 

La adaptabilidad alta es poco frecuente en todos los grupos, mientras que la adaptabilidad baja presenta valores significativos 
especialmente en los rangos de 16–20 y 21–25 años, lo que sugiere dificultades relevantes en la transición a entornos educativos digitales
en estas edades.
*/

-- 6.3. Adaptabilidad vs Nivel educativo

SELECT 
    ds.education_level,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_student ds ON f.student_id = ds.student_id
GROUP BY ds.education_level , f.adaptivity_level
ORDER BY ds.education_level , total_registros DESC;

/*
En etapas escolares, la educación online funciona de manera intermedia, muy dependiente del acompañamiento y recursos.
Aunque cabría esperar mayor autonomía digital, la adaptabilidad universitaria no es significativamente mejor que en niveles previos.
En la etapa del instituto, parece ser el menos adaptado a la educación online, posiblemente por menor flexibilidad metodológica.

En conclusión, la adaptabilidad a la educación online no mejora necesariamente con el nivel educativo. Tanto en niveles escolares como 
universitarios predomina una adaptación moderada, mientras que el nivel College presenta mayores dificultades, con una alta concentración 
de baja adaptabilidad.
*/

-- 6.4. Adaptabilidad vs Tipo de institución

SELECT 
    di.institution_type,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_institution di ON f.institution_id = di.institution_id
GROUP BY di.institution_type, f.adaptivity_level
ORDER BY di.institution_type, total_registros DESC;

/*
En instituciones gubernamentales (públicas): 
	- La adaptabilidad baja es claramente dominante.
    - La adaptabilidad alta es residual.
Es decir, la transición a la educación online parece haber sido más compleja y desigual en el sector público.

¿Posibles causas?
	- Menor acceso a recursos tecnológicos
	- Infraestructura digital más limitada
	- Menor flexibilidad metodológica
	- Mayor dependencia de modelos presenciales tradicionales
    
En instituciones no gubernamentales (privadas):
	- La adaptabilidad moderada es la más frecuente.
    - Hay una presencia significativa de adaptabilidad alta.
    - La adaptabilidad baja existe, pero no es mayoritaria.
    
Por lo que muestran una mejor capacidad de adaptación al modelo online, con más estudiantes situados en niveles moderados y altos.
Puede ser debido a:
	- Mayor inversión en plataformas digitales
    - Metodologías más flexibles
    - Mejor soporte tecnológico y pedagógico

Esto sugiere que el tipo de institución es un factor relevante en la adaptabilidad a la educación online, observándose mejores resultados 
en instituciones no gubernamentales frente a las gubernamentales.
*/

-- 6.5. Adaptabilidad vs Condición financiera

SELECT 
    dse.financial_condition,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_socio_economic dse ON f.socio_id = dse.socio_id
GROUP BY dse.financial_condition, f.adaptivity_level
ORDER BY dse.financial_condition, total_registros DESC;

/*
Estudiantes con una condición financiera MEDIA (grupo mayoritario):
	- Hay 501 estudantes con una adaptabilad media (el valor más alto).
    - 341 con una baja adaptación (muy relevante)
    - La adaptación alta es el más minoritario con 36 estudiantes.alter
Esto sugiere que no están excluidos del entorno digital pero no tienen condiciones óptimas y se adaptan razonablemente.

Estudiantes con una condición financiera POBRE:
	- Domina los estudiantes con adaptación baja contando con 129.
Por lo que podemos observar que presentan más dificultades estructurales claras.

Estudiantes con una condición financiera ALTA:
	- Predomina el grupo de adaptación alta con 42 estudiantes siendo la baja casi inexistente.
Por lo tanto, se adaptan mejor al entorno online ya que disponen de tecnología adecuada, buena conectividad, etc.

En conclusión:

El análisis de la adaptabilidad a la educación online según la condición financiera muestra una relación directa entre los recursos 
económicos y el nivel de adaptación. Los estudiantes con una condición financiera alta presentan mayoritariamente niveles de adaptabilidad
elevados, mientras que aquellos con menores recursos se concentran en niveles bajos. Los estudiantes con condición financiera media
muestran una adaptabilidad principalmente moderada, lo que sugiere un acceso parcial a los recursos necesarios para un aprovechamiento 
óptimo del aprendizaje online.
*/

--  Condición financiera vs Tipo de institución

SELECT 
    dse.financial_condition,
    di.institution_type,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_socio_economic dse ON f.socio_id = dse.socio_id
JOIN dim_institution di ON f.institution_id = di.institution_id
GROUP BY dse.financial_condition, di.institution_type
ORDER BY dse.financial_condition, total_registros DESC;

/*
El análisis conjunto de la condición financiera y el tipo de institución muestra una predominancia de estudiantes en 
instituciones no gubernamentales en todos los niveles económicos. Esta tendencia es especialmente notable en los estudiantes
 con condición financiera media, lo que sugiere que la elección institucional no depende únicamente del nivel económico, 
 sino también de factores como la accesibilidad, la oferta educativa y la infraestructura disponible, aspectos que pueden influir 
 indirectamente en la adaptabilidad a la educación online.
*/

-- 6.6. Adaptabilidad vs Load Shedding

SELECT 
    dse.load_shedding,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_socio_economic dse 
    ON f.socio_id = dse.socio_id
GROUP BY dse.load_shedding, f.adaptivity_level
ORDER BY dse.load_shedding, total_registros DESC;

/*
El análisis entre la incidencia del load shedding y el nivel de adaptabilidad a la educación online evidencia 
una relación negativa clara. En contextos con alta frecuencia de cortes eléctricos, los estudiantes presentan 
mayoritariamente niveles de adaptabilidad bajos, mientras que la adaptabilidad alta es residual. 
Por el contrario, en entornos con suministro eléctrico más estable, predominan niveles de adaptabilidad moderada 
y se observa una mayor presencia de adaptabilidad alta. Estos resultados sugieren que la estabilidad energética 
es un factor estructural clave para el éxito del aprendizaje online.
*/

-- 6.7. Adaptabilidad vs Acceso tecnológico

-- Tipo de dispositivo

SELECT 
    dt.device,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_tech dt 
    ON f.tech_id = dt.tech_id
GROUP BY dt.device, f.adaptivity_level
ORDER BY dt.device, total_registros DESC;

/*
El análisis del nivel de adaptabilidad según el tipo de dispositivo muestra que el uso de ordenadores se asocia 
a mejores niveles de adaptación a la educación online, mientras que el uso predominante del teléfono móvil presenta una mayor 
concentración de adaptabilidad baja. Aunque el móvil facilita el acceso al aprendizaje digital, sus limitaciones técnicas y de 
usabilidad pueden afectar negativamente a la experiencia educativa. El uso de tablets es minoritario y no permite extraer conclusiones 
significativas.
*/

-- Tipo de internet

SELECT 
    dt.internet_type,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_tech dt 
    ON f.tech_id = dt.tech_id
GROUP BY dt.internet_type, f.adaptivity_level
ORDER BY dt.internet_type, total_registros DESC;

/*
El análisis del nivel de adaptabilidad según el tipo de acceso a Internet evidencia que las conexiones WiFi se asocian 
a mejores niveles de adaptación a la educación online, con una mayor presencia de adaptabilidad alta y una menor concentración 
de casos de adaptabilidad baja. Por el contrario, el uso de datos móviles, aunque facilita el acceso, presenta limitaciones que 
pueden afectar negativamente a la continuidad y calidad del aprendizaje digital.
*/

-- Uso de LMS propios

SELECT 
    dt.self_lms,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_tech dt 
    ON f.tech_id = dt.tech_id
GROUP BY dt.self_lms, f.adaptivity_level
ORDER BY dt.self_lms, total_registros DESC;

/*
El análisis del nivel de adaptabilidad según el uso de un LMS propio muestra que las instituciones que cuentan con 
plataformas de aprendizaje estructuradas presentan mejores niveles de adaptación a la educación online. 
La presencia de un LMS se asocia con una mayor proporción de adaptabilidad alta y una reducción significativa de los casos 
de adaptabilidad baja, lo que sugiere que la organización y centralización del proceso educativo es un factor clave para el 
éxito del aprendizaje digital.
*/

-- 6.8. Adaptabilidad vs Localización (sintética)

SELECT 
    dl.environment_type,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_localization dl 
    ON f.localization_id = dl.localization_id
GROUP BY dl.environment_type, f.adaptivity_level
ORDER BY dl.environment_type, total_registros DESC;

/*
El análisis de la adaptabilidad según el tipo de entorno muestra diferencias significativas en los niveles de adaptación 
a la educación online. Los entornos semiurbanos concentran principalmente niveles de adaptabilidad moderada, mientras que 
los entornos rurales presentan una distribución más equilibrada entre los distintos niveles. Por su parte, los entornos urbanos, 
definidos en este estudio por una menor incidencia de problemas infraestructurales, muestran una mayor presencia de adaptabilidad baja. 
Dado que el tipo de entorno ha sido generado de forma sintética a partir de variables socioeconómicas, estos resultados deben interpretarse 
como una representación del impacto del contexto estructural en la adaptabilidad, más que como una relación causal independiente.

-----------------------------------------------------------------------

7. ANÁLISIS AVANZADO
*/

-- 7.1. Ranking comparando la tecnología y la adaptabilidad

WITH tech_adaptability AS (
    SELECT 
        dt.device,
        dt.internet_type,
        f.adaptivity_level,
        COUNT(*) AS total
    FROM fact_adaptability f
    JOIN dim_tech dt ON f.tech_id = dt.tech_id
    GROUP BY dt.device, dt.internet_type, f.adaptivity_level
),
ranked_tech AS (
    SELECT *,
		RANK() OVER (PARTITION BY device ORDER BY total DESC) AS ranking
    FROM tech_adaptability
)
SELECT *
FROM ranked_tech
WHERE ranking = 1
ORDER BY total DESC;

/*
El análisis de ranking por combinación de tipo de dispositivo y acceso a internet muestra que el nivel de adaptabilidad 
moderado es el más frecuente en todos los casos. Este resultado sugiere que, independientemente de las condiciones tecnológicas, 
la mayoría de los estudiantes logra adaptarse funcionalmente a la educación online, aunque sin alcanzar niveles óptimos de adaptación. 
La tecnología, por tanto, actúa como un facilitador, pero no garantiza por sí sola una alta adaptabilidad.
*/

-- 7.2. Ranking de factores socioeconómicos

WITH socio_adaptability AS (
    SELECT 
        dse.financial_condition,
        dl.environment_type,
        f.adaptivity_level,
        COUNT(*) AS total
    FROM fact_adaptability f
    JOIN dim_socio_economic dse ON f.localization_id = dse.localization_id
    JOIN dim_localization dl ON dse.localization_id = dl.localization_id
    GROUP BY dse.financial_condition, dl.environment_type, f.adaptivity_level
),
ranked_socio AS (
    SELECT *,
        RANK() OVER (PARTITION BY financial_condition ORDER BY total DESC) AS ranking
    FROM socio_adaptability
)
SELECT *
FROM ranked_socio
WHERE ranking = 1;

/*
El ranking por factores socioeconómicos revela que el entorno y la condición financiera juntos condicionan la adaptabilidad: 
la clase media en entornos semiurbanos logra adaptabilidad moderada, mientras que tanto los estudiantes pobres como los ricos en entornos 
rurales presentan adaptabilidad baja. Esto sugiere que el entorno físico/infraestructural puede ser un factor limitante incluso 
para quienes cuentan con mayores recursos económicos.
*/

-- 7.3. Evolución temporal (sintético)

-- ¿Cuántos estudiantes en total tienen una adaptabilidad baja por cada año?

SELECT 
    dc.year,
    f.adaptivity_level,
    COUNT(*) AS total_registros
FROM fact_adaptability f
JOIN dim_calendar dc ON f.calendar_id = dc.calendar_id
WHERE f.adaptivity_level = 'Low'
GROUP BY dc.year, f.adaptivity_level
ORDER BY total_registros DESC;

/*
El año con más estudiantes con baja adaptabilidad es en 2022 seguido de 2021 y con menos es el año 2024. Esto puede deberse a
que cada año ha ido mejorando las infraestructuras tecnológicas facilitando la accesibilidad y las plataformas online.
*/

-- 7.4. Proporción de adaptabilidad por ámbito socio económico

SELECT 
    dl.environment_type,
    dse.financial_condition,
    dt.internet_type,
    COUNT(*) AS estudiantes_baja_adaptabilidad
FROM fact_adaptability f
JOIN dim_socio_economic dse ON f.socio_id = dse.socio_id
JOIN dim_localization dl ON dse.localization_id = dl.localization_id
JOIN dim_tech dt ON f.tech_id = dt.tech_id
WHERE f.adaptivity_level = 'Low'
GROUP BY 
    dl.environment_type,
    dse.financial_condition,
    dt.internet_type
ORDER BY estudiantes_baja_adaptabilidad DESC;

/*
El análisis conjunto del entorno, la condición financiera y el tipo de acceso a internet muestra que la mayor concentración de 
estudiantes se encuentra en entornos semiurbanos con condición financiera media, utilizando tanto datos móviles como Wifi. 
En entornos rurales, los estudiantes con bajos recursos dependen mayoritariamente de datos móviles, mientras que incluso los estudiantes 
con mayor capacidad económica presentan baja representación, lo que refuerza la idea de que el entorno limita el acceso tecnológico 
más allá de la condición financiera. Por su parte, los entornos urbanos muestran una distribución más equilibrada del tipo de conexión, 
reduciendo parcialmente la brecha digital.

-----------------------------------------------------------------------

8. RESUMEN DE LOS DATOS
*/

CREATE OR REPLACE VIEW students_adaptability_summary AS
SELECT 
    dl.environment_type,
    dse.financial_condition,
    dt.internet_type,
    dt.device,
    di.institution_type,
    ds.age_range,
    ds.education_level,
    f.adaptivity_level,
    COUNT(*) AS total_estudiantes
FROM fact_adaptability f
JOIN dim_socio_economic dse ON f.socio_id = dse.socio_id
JOIN dim_localization dl ON dse.localization_id = dl.localization_id
JOIN dim_tech dt ON f.tech_id = dt.tech_id
JOIN dim_institution di ON  di.institution_id = f.institution_id
JOIN dim_student ds ON ds.student_id = f.student_id
GROUP BY 
    dl.environment_type,
    dse.financial_condition,
    dt.internet_type,
    dt.device,
    di.institution_type,
    ds.age_range,
    ds.education_level,
    f.adaptivity_level
ORDER BY total_estudiantes DESC;

SELECT 
    *
FROM
    students_adaptability_summary;

/*
El grueso de los estudiantes pertenece a contextos semiurbanos de clase media, accede a la educación online principalmente mediante 
dispositivos móviles y datos móviles, y presenta niveles de adaptabilidad mayoritariamente moderados.

La alta adaptabilidad no depende únicamente del entorno, sino de la combinación de recursos tecnológicos, madurez educativa y 
estabilidad económica.

Podemos concluir que, el análisis conjunto de los factores socioeconómicos, tecnológicos y educativos muestra que la adaptabilidad a la 
educación online es el resultado de la acumulación de condiciones estructurales. Los perfiles con mayor adaptabilidad se concentran en 
estudiantes universitarios con acceso a Wifi y dispositivos más robustos, mientras que la baja adaptabilidad aparece principalmente en 
estudiantes jóvenes de entornos rurales con bajos recursos y acceso limitado a través de datos móviles.

A continuación, para poder realizar un filtrado más avanzado definiendo variables específicas, se crea una función a raíz de la vista
creada anteriormente.
*/
 
DELIMITER $$

CREATE FUNCTION fn_adaptability (
    p_environment VARCHAR(20),
    p_financial_condition VARCHAR(20),
    p_internet_type VARCHAR(20),
    p_device VARCHAR(20),
    p_institution_type VARCHAR(20),
    p_age_range VARCHAR(20),
    p_education_level VARCHAR(20)
)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE adaptivity VARCHAR(20);
    SELECT 
    adaptivity_level
	INTO adaptivity
	FROM students_adaptability_summary 
    WHERE environment_type = p_environment
		AND financial_condition = p_financial_condition
        AND internet_type = p_internet_type
        AND device = p_device
        AND institution_type = p_institution_type
        AND age_range = p_age_range
        AND education_level = p_education_level
	GROUP BY adaptivity_level
    ORDER BY COUNT(*) DESC
    LIMIT 1;
    
    RETURN adaptivity;
END$$

DELIMITER ;

SELECT 
	'Urban / Mid / Wifi / Mobile / Government / 16-20 / College' AS contexto,
	fn_adaptability('Urban', 'Mid', 'Wifi', 'Mobile', 'Government', '16-20', 'College') AS adaptabilidad;

/*
-----------------------------------------------------------------------

9. CONCLUSIONES

El presente proyecto ha tenido como objetivo analizar los factores que influyen en la adaptabilidad de los estudiantes a la educación 
online, combinando variables sociodemográficas, socioeconómicas, tecnológicas y educativas a partir de un enfoque analítico basado en 
un modelo dimensional.

A lo largo del análisis, se ha observado que la adaptabilidad a la educación online no depende de un único factor, sino que es el 
resultado de la interacción entre múltiples condiciones estructurales.

En primer lugar, el análisis por rangos de edad muestra que la mayor parte de los estudiantes se concentra en los tramos de 11–15 y 21–25 
años, siendo estos últimos los que presentan mejores niveles de adaptabilidad. Esto sugiere que la madurez académica y la experiencia 
previa con entornos digitales juegan un papel relevante en la capacidad de adaptación.

Desde el punto de vista socioeconómico, la condición financiera aparece como uno de los factores más determinantes. Los estudiantes con 
una situación económica media concentran la mayoría de los casos de adaptabilidad moderada, mientras que los perfiles con condición 
económica baja presentan una mayor proporción de adaptabilidad baja. En contraste, los estudiantes con mejor situación financiera 
muestran una mayor presencia de adaptabilidad alta, especialmente cuando se combina con acceso tecnológico adecuado.

El tipo de entorno refuerza esta tendencia. Los entornos semiurbanos concentran la mayor parte de los estudiantes y presentan, en general,
niveles de adaptabilidad moderados. Por su parte, los entornos rurales registran una mayor incidencia de adaptabilidad baja, 
especialmente cuando se combinan con limitaciones económicas y tecnológicas. Los entornos urbanos, aunque con menor volumen, 
muestran una distribución más equilibrada y mejores resultados relativos.

En cuanto a los factores tecnológicos, el acceso a internet y el tipo de dispositivo resultan clave. El uso de datos móviles y 
dispositivos móviles se asocia mayoritariamente con niveles de adaptabilidad baja o moderada, mientras que el acceso a Wifi y 
dispositivos como ordenadores se relaciona con una mayor adaptabilidad. Esto evidencia la importancia de una infraestructura tecnológica 
estable para un aprendizaje online eficaz.

El análisis del uso de plataformas LMS refuerza esta idea: los estudiantes que utilizan sistemas de gestión del aprendizaje presentan 
una mayor proporción de adaptabilidad alta en comparación con aquellos que no los utilizan, lo que sugiere que la estructuración del 
entorno educativo digital mejora la experiencia de aprendizaje.

El análisis conjunto de todos los factores ha permitido identificar perfiles completos de estudiantes. 

Los perfiles más frecuentes corresponden a estudiantes de entornos semiurbanos, con condición financiera media, acceso a internet 
mediante datos móviles, uso de dispositivos móviles y adaptabilidad moderada.

Por el contrario, los perfiles con baja adaptabilidad se concentran en estudiantes jóvenes de entornos rurales, con condición económica 
baja, acceso limitado a internet y dispositivos menos adecuados. Los casos de alta adaptabilidad, aunque menos numerosos, aparecen 
asociados a estudiantes universitarios, con mejor situación económica, acceso a Wifi y dispositivos más robustos, incluso en entornos 
no urbanos.

Este enfoque confirma que la adaptabilidad a la educación online responde a una acumulación de ventajas o desventajas, más que a un 
único elemento aislado.
*/
 
 
 
 
/*
PRÓXIMOS PASOS:
	

PUNTOS IMPORTANTES DEL ANÁLISIS:
	- El tipo de institución es un factor relevante en la adaptabilidad a la educación online, observándose mejores resultados 
	en instituciones no gubernamentales frente a las gubernamentales. 
    - El análisis de la adaptabilidad a la educación online según la condición financiera muestra una relación directa entre los recursos 
	económicos y el nivel de adaptación
    - Análisis de la adaptabilidad con load shedding tienen una relación con tendencia negativa. Mas cortes de luz, menos adaptabilidad, reforzando
    los análisis previos de condición financiera e insitutición y muestra que la brecha digital no es solo tecnológica, sino infraestructural.
    - Análisis de adaptabilidad con el tipo de dispositivo usado: condición financiera → quién puede acceder a un ordenador
	load shedding → estabilidad para usar dispositivos
	tipo de institución → infraestructura disponible
    - Análisis de adaptabilidad con el tipo de acceso a internet: 
		el impacto del tipo de dispositivo (móvil + datos = doble limitación)
		la condición financiera
		la infraestructura tecnológica del entorno
	- La adaptabilidad no depende solo del estudiante, sino del ecosistema educativo en el que se desarrolla
    
INFO IMPORTANTE:
	- Poner en el README que hay que importar el csv en la base de datos para que se pueda ejecutar las tablas. (poner pasos que hay que
    seguir)
    
PARA LA PRESENTACIÓN:
	- Vistas creadas en distribución por edad y en adaptabilidad por edad: La distribución porcentual por rango de edad se calcula 
    mediante funciones ventana, mientras que los niveles de adaptabilidad se obtienen mediante agregaciones condicionales.
*/