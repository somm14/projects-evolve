USE online_education;

-- Se insertan los datos procedentes del archivo en crudo "students_adaptability_level_online_education.csv"

/* -------------------------------------------
Insertar datos en la tabla DIM_STUDENT 
------------------------------------------- */

INSERT INTO dim_student (gender, age_range, education_level)
SELECT DISTINCT
    Gender,
    Age,
    `Education Level` -- Comillas invertidas para poder "llamar" a la columna que quiero obtener la información
FROM students_adaptability_level_online_education;

/* -------------------------------------------
Insertar datos en la tabla DIM_INSTITUTION 
------------------------------------------- */

INSERT INTO dim_institution (institution_type, it_student)
SELECT DISTINCT
    `Institution Type`,
    `IT Student` 
FROM students_adaptability_level_online_education;

/* -------------------------------------------
Insertar datos en la tabla DIM_TECH
------------------------------------------- */

INSERT INTO dim_tech (internet_type, network_type, device, self_lms)
SELECT DISTINCT
    `Internet Type`,
    `Network Type`,
    Device,
    `Self LMS`
FROM students_adaptability_level_online_education;

/* -------------------------------------------
Insertar datos en la tabla DIM_LOCALIZATION
------------------------------------------- */

INSERT INTO dim_localization (environment_type)
VALUES
    ('Urban'),
    ('Semi-Urban'),
    ('Rural');

/* -------------------------------------------
Insertar datos en la tabla DIM_SOCIO-ECONOMIC
------------------------------------------- */

INSERT INTO dim_socio_economic (financial_condition, load_shedding, location)
SELECT DISTINCT
    `Financial Condition`,
    `Load-Shedding`,
    Location
FROM students_adaptability_level_online_education;

-- Asigno localizaciones sintéticas distribuyéndolo de forma controlada, es decir, si es urbano lo relaciono con mejor infraestructura,
-- si es rural, más problemas.

UPDATE dim_socio_economic
SET localization_id = 
	CASE
		WHEN load_shedding = 'High' THEN 1   									 -- Urban
		WHEN load_shedding = 'Low' AND financial_condition = 'Mid' THEN 2 -- Semi-Urban
		ELSE 3                            									 -- Rural
	END
WHERE localization_id IS NULL;

/* -------------------------------------------
Insertar datos en la tabla DIM_CALENDAR
------------------------------------------- */
-- Inserto los números del 0 al 9999 en mi tabla de números únicamente para crear los datos sintéticos de dim_calendar

SELECT COUNT(*) FROM students_adaptability_level_online_education; -- 1205 registros

INSERT INTO numbers (n)
SELECT a.n + b.n * 10 + c.n * 100 + d.n * 1000 AS n
FROM 
    (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
    (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b,
    (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c,
     (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d;
     
select * from numbers order by n desc;

INSERT INTO dim_calendar (calendar_id, full_date, year, month, quarter, day_of_week)
SELECT
    ROW_NUMBER() OVER () AS calendar_id, -- Genero para el ID números por "ranking"
    DATE_ADD('2021-01-01', INTERVAL n DAY) AS full_date, -- Genero fechas a partir del 2021 y que sea un intervalo de un día
    YEAR(DATE_ADD('2021-01-01', INTERVAL n DAY)) AS year,
    MONTH(DATE_ADD('2021-01-01', INTERVAL n DAY)) AS month,
    QUARTER(DATE_ADD('2021-01-01', INTERVAL n DAY)) AS quarter,
    DAYNAME(DATE_ADD('2021-01-01', INTERVAL n DAY)) AS day_of_week
FROM numbers
WHERE n < 1205; -- Número de registros que hay en el dataset en crudo

select * from dim_calendar order by calendar_id desc;

DROP TABLE IF EXISTS numbers; -- Se borra la tabla creada únicamente para generar fechas sintéticas

/* -------------------------------------------
Insertar datos en la tabla FACT_ADAPTABILITY
------------------------------------------- */

INSERT INTO fact_adaptability (
    student_id,
    institution_id,
    tech_id,
    socio_id,
    class_duration,
    adaptivity_level
)
SELECT
    s.student_id,
    i.institution_id,
    t.tech_id,
    se.socio_id,
    st.`Class Duration`,
    st.`Adaptivity Level`
FROM students_adaptability_level_online_education st
JOIN dim_student s
  ON st.Gender = s.gender
 AND st.Age = s.age_range
 AND st.`Education Level` = s.education_level
JOIN dim_institution i
  ON st.`Institution Type` = i.institution_type
 AND st.`IT Student` = i.it_student
JOIN dim_tech t
  ON st.`Internet Type` = t.internet_type
 AND st.`Network Type` = t.network_type
 AND st.Device = t.device
 AND st.`Self LMS` = t.self_lms
JOIN dim_socio_economic se
  ON st.`Financial Condition` = se.financial_condition
 AND st.`Load-shedding` = se.load_shedding
 AND st.Location = se.location;

-- Inserto los datos sintéticos de las fechas y del entorno.
UPDATE fact_adaptability
SET calendar_id = fact_id
WHERE calendar_id IS NULL AND fact_id > 0;

UPDATE fact_adaptability f
JOIN dim_socio_economic s
ON f.socio_id = s.socio_id
SET f.localization_id = s.localization_id;

SELECT * FROM fact_adaptability;

USE online_education;
