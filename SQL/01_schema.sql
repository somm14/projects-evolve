-- Genero la base de datos desde 0
DROP DATABASE IF EXISTS online_education;
CREATE DATABASE IF NOT EXISTS online_education;

-- Lo activo
USE online_education;

-- Creo las tablas DIMENSIONES

DROP TABLE IF EXISTS dim_student;
CREATE TABLE IF NOT EXISTS dim_student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL, 			-- Boy | Girl
    age_range VARCHAR(20) NOT NULL,
    education_level VARCHAR(50) NOT NULL,	-- School | College | University

    CONSTRAINT uq_student UNIQUE (gender, age_range, education_level) -- Se evita duplicados
);


DROP TABLE IF EXISTS dim_institution;
CREATE TABLE IF NOT EXISTS dim_institution (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_type VARCHAR(50) NOT NULL,	-- Government | Non Goverment
    it_student VARCHAR(10) NOT NULL, 		-- Yes | No

    CONSTRAINT uq_institution UNIQUE (institution_type, it_student)
);

DROP TABLE IF EXISTS dim_tech;
CREATE TABLE IF NOT EXISTS dim_tech (
    tech_id INT AUTO_INCREMENT PRIMARY KEY,
    internet_type VARCHAR(20) NOT NULL,	-- Mobile Data | Wifi
    network_type VARCHAR(20) NOT NULL,	-- 4G | 3G
    device VARCHAR(30) NOT NULL,		-- Mobile | Computer | Tab
    self_lms VARCHAR(10) NOT NULL,		-- Yes | No

    CONSTRAINT uq_tech UNIQUE (internet_type, network_type, device, self_lms)
);

DROP TABLE IF EXISTS dim_localization;
CREATE TABLE IF NOT EXISTS dim_localization ( -- Tabla sintética
    localization_id INT AUTO_INCREMENT PRIMARY KEY,
    environment_type VARCHAR(20) NOT NULL, -- Urban | Semi-Urban | Rural
    
    CONSTRAINT uq_environment UNIQUE (environment_type)
);

DROP TABLE IF EXISTS dim_socio_economic;
CREATE TABLE IF NOT EXISTS dim_socio_economic (
    socio_id INT AUTO_INCREMENT PRIMARY KEY,
    financial_condition VARCHAR(20) NOT NULL, 	-- Rich | Mid | Poor
    load_shedding VARCHAR(10) NOT NULL,			-- High | Low
    location VARCHAR(20) NOT NULL,				-- Yes | No

    CONSTRAINT uq_socio UNIQUE (financial_condition, load_shedding, location)
);

-- Modifico la tabla DIM_SOCIO_ECONOMIC para añadir la localization_id conforme al tipo 
-- del entorno.

ALTER TABLE dim_socio_economic
ADD COLUMN localization_id INT,
ADD CONSTRAINT fk_socio_localization
FOREIGN KEY (localization_id)
REFERENCES dim_localization(localization_id);

DROP TABLE IF EXISTS dim_calendar;
CREATE TABLE IF NOT EXISTS dim_calendar ( -- Tabla sintética
    calendar_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL
);

-- Creo una tabla solo con números del 0 al 9999
DROP TABLE IF EXISTS numbers;
CREATE TABLE numbers (
    n INT PRIMARY KEY
);

-- Creo la tabla de HECHOS
DROP TABLE IF EXISTS fact_adaptability;
CREATE TABLE IF NOT EXISTS fact_adaptability (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    institution_id INT NOT NULL,
    tech_id INT NOT NULL,
    socio_id INT NOT NULL,
	class_duration VARCHAR(20),				-- Rangos
    adaptivity_level VARCHAR(20) NOT NULL,	-- High | Moderate | Low
    
    CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES dim_student(student_id),
    CONSTRAINT fk_institution FOREIGN KEY (institution_id) REFERENCES dim_institution(institution_id),
    CONSTRAINT fk_tech FOREIGN KEY (tech_id) REFERENCES dim_tech(tech_id),
    CONSTRAINT fk_socio FOREIGN KEY (socio_id) REFERENCES dim_socio_economic(socio_id)
);

-- Añado los datos sintéticos del entorno y de las fechas y creo las claves foráneas
ALTER TABLE fact_adaptability
ADD COLUMN calendar_id INT,
ADD COLUMN localization_id INT,
ADD CONSTRAINT fk_fact_localization
FOREIGN KEY (localization_id)
REFERENCES dim_localization(localization_id);


-- Optimiza JOINs con la dimensión de estudiantes
CREATE INDEX idx_fact_student
ON fact_adaptability (student_id);

-- Optimiza análisis por tipo de institución
CREATE INDEX idx_fact_institution
ON fact_adaptability (institution_id);

-- Optimiza análisis por entorno tecnológico
CREATE INDEX idx_fact_tech
ON fact_adaptability (tech_id);

-- Optimiza análisis socioeconómicos
CREATE INDEX idx_fact_socio
ON fact_adaptability (socio_id);

-- Optimiza análisis temporales
CREATE INDEX idx_fact_calendar
ON fact_adaptability (calendar_id);

