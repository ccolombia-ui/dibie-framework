# Análisis de Tabla Maestra - Datos Financieros

## 📊 Resumen Ejecutivo

**Fecha de análisis:** 2025-11-07  
**Fuente:** Google Sheets (maestro)  
**Framework:** DIBIE - Data Intelligence Business Intelligence Engine

---

## 📈 Estadísticas Generales

- **Total de registros:** 22 instituciones educativas
- **Total de columnas:** 164 campos
- **Formato de datos:** CSV (60.9 KB)

---

## 🔑 Campos Clave Identificados

### Identificadores (PK Candidates)
- `row_id` - 22 valores únicos (100% único)
- `cod_colegio` - 22 valores únicos (100% único) ✅ **Recomendado como PK**
- `direccion` - 22 valores únicos (100% único)
- `email` - 22 valores únicos (100% único)
- `area_lote` - 22 valores únicos (100% único)

### Información Institucional
- `nombre_colegio` - 19 valores únicos (alta cardinalidad)
- `municipio` - 21 valores únicos (casi único)

### Datos Financieros
- `valor_lote`
- `INGRESOS`
- `INGRESOS DE OPERACIÓN (2-6)`
- `Valor anual servicio educativo (3+4+5)`
- `TOTAL INGRESOS (1+9)`
- `EGRESOS`
- `GASTOS OPERACIONALES (12+35)`
- Y más...

---

## 🗂️ Estructura de Tablas Atómicas Propuesta

### 1. **maestro_instituciones** (Tabla Maestra)
```sql
CREATE TABLE maestro_instituciones (
    cod_colegio VARCHAR(255) PRIMARY KEY,
    nombre_colegio VARCHAR(255)
);
```
**Propósito:** Catálogo principal de instituciones educativas  
**Filas estimadas:** 22

---

### 2. **ubicacion_geografica** (Dimensión Geográfica)
```sql
CREATE TABLE ubicacion_geografica (
    ubicacion_id INT PRIMARY KEY AUTO_INCREMENT,
    cod_colegio VARCHAR(255) FOREIGN KEY,
    direccion VARCHAR(255),
    municipio VARCHAR(255),
    -- Campos adicionales detectados
);
```
**Propósito:** Información geográfica y de localización  
**Filas estimadas:** 22

---

### 3. **hechos_financieros** (Tabla de Hechos) ⭐
```sql
CREATE TABLE hechos_financieros (
    hecho_id INT PRIMARY KEY AUTO_INCREMENT,
    cod_colegio VARCHAR(255) FOREIGN KEY,
    fecha_id INT FOREIGN KEY,
    valor_lote DECIMAL(15,2),
    ingresos DECIMAL(15,2),
    egresos DECIMAL(15,2),
    total_ingresos DECIMAL(15,2),
    -- Más campos financieros...
);
```
**Propósito:** Registro de transacciones y valores financieros  
**Tipo:** Fact Table (análisis OLAP)  
**Filas estimadas:** 22 (podría crecer con datos históricos)

---

### 4. **dim_tiempo** (Dimensión Temporal)
```sql
CREATE TABLE dim_tiempo (
    fecha_id INT PRIMARY KEY,
    ano INT,
    periodo VARCHAR(50),
    numero_estudiantes INT,
    costo_por_estudiante DECIMAL(10,2)
);
```
**Propósito:** Dimensión de tiempo para análisis histórico  
**Filas estimadas:** Variable (depende del rango temporal)

---

### 5-10. **Dimensiones Adicionales**
- `dim_asesor_del_sector_defensa_09_gestion_comunidad`
- `dim_servicios_prestados_por_terceros`
- `dim_servicios_generales_prestados_por_terceros`
- `dim_servicios_de_apoyo_prestados_por_terceros`
- `dim_servicios_administrativos_prestados_por_terceros`
- `dim_gastos_operacionales_anuales`

---

## 📁 Categorización de Columnas

| Categoría | Cantidad | Ejemplos |
|-----------|----------|----------|
| **INSTITUCIONES** | 2 | cod_colegio, nombre_colegio |
| **UBICACION** | 4 | direccion, municipio |
| **FINANCIERO** | 10 | valor_lote, INGRESOS, EGRESOS |
| **TEMPORAL** | 2 | numero_estudiantes, costo_por_estudiante |
| **CATEGORIAS** | 6 | servicios_terceros, gastos_operacionales |
| **OTROS** | 140 | Varios campos de personal, roles, etc. |

---

## ⚠️ Hallazgos Importantes

### Columnas Duplicadas
Se detectaron **columnas con nombres duplicados**:
- `Preescolar` (aparece 2 veces)
- `Basica` (aparece 1 vez)
- `Media` (aparece 2 veces)
- `Salarios Básicos` (aparece 4 veces)
- `Prestaciones` (aparece 4 veces)
- `Aportes de Nómina` (aparece 4 veces)
- `Material no fungible` (aparece 2 veces)
- `Vehículos` (aparece 2 veces)

**Recomendación:** Revisar y renombrar con contexto específico:
- `Preescolar_Grado` vs `Preescolar_Personal`
- `Salarios_Básicos_Docentes` vs `Salarios_Básicos_Administrativos`

### Datos Faltantes
- Una institución registrada como "FALTA INFORMACION DE NUESTRA SEÑORA DE FATIMA DE BOGOTA"
- `cod_colegio` con valores vacíos en algunas filas

---

## 📦 Archivos Generados

1. **diccionario_datos.json** (61 KB)
   - Metadata completa de cada columna
   - Tipos de datos, cardinalidad, valores de muestra

2. **propuesta_tablas_atomicas.json** (3.4 KB)
   - Diseño de base de datos normalizada
   - Relaciones entre tablas

3. **schema_sql.sql** (2.7 KB)
   - Script DDL para crear tablas
   - Listo para ejecutar en MySQL/PostgreSQL

4. **maestro_financiero.csv** (22.1 KB)
   - Datos completos en formato CSV
   - Columnas duplicadas renombradas automáticamente

---

## 🎯 Próximos Pasos Recomendados

### Fase 1: Limpieza de Datos
1. ✅ Corregir nombres de columnas duplicadas
2. ✅ Completar información faltante (NUESTRA SEÑORA DE FATIMA)
3. ✅ Validar códigos DANE de instituciones

### Fase 2: Normalización
1. 📊 Crear tabla `maestro_instituciones` con PK en `cod_colegio`
2. 📊 Separar datos de ubicación en tabla independiente
3. 📊 Crear tabla de hechos financieros con FK a instituciones

### Fase 3: Enriquecimiento
1. 🌍 Agregar coordenadas geográficas (latitud, longitud)
2. 📅 Incorporar dimensión temporal (año fiscal, vigencia)
3. 📈 Crear vistas materializadas para KPIs frecuentes

### Fase 4: Visualización
1. 📊 Dashboard en Apache Superset con:
   - Mapa de instituciones por municipio
   - Gráficos de barras: Ingresos vs Egresos
   - Análisis de costo por estudiante
   - Distribución presupuestal

---

## 🔧 Uso de Archivos

### Cargar Diccionario de Datos
```python
import json
with open('data/processed/diccionario_datos.json', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)
print(data_dict['total_columns'])  # 164
```

### Cargar Propuesta de Tablas
```python
import json
with open('data/processed/propuesta_tablas_atomicas.json', 'r', encoding='utf-8') as f:
    tables = json.load(f)
print(tables['maestro_instituciones']['columns'])
```

### Ejecutar Schema SQL
```bash
# MySQL
mysql -u usuario -p nombre_db < data/processed/schema_sql.sql

# PostgreSQL
psql -U usuario -d nombre_db -f data/processed/schema_sql.sql
```

### Cargar Datos CSV
```python
import pandas as pd
df = pd.read_csv('data/processed/maestro_financiero.csv')
print(df.shape)  # (22, 164)
```

---

## 📞 Contacto

**Framework:** DIBIE - Data Intelligence Business Intelligence Engine  
**Repositorio:** https://github.com/ccolombia-ui/dibie-framework  
**Documentación:** Ver README.md en raíz del proyecto

---

## 📝 Notas Técnicas

- **Autenticación:** Google Service Account configurada
- **Email servicio:** aksobhya-googlesheet-806@aksobhya.iam.gserviceaccount.com
- **Formato origen:** Google Sheets (GID: 1897725171)
- **Codificación:** UTF-8
- **Separador CSV:** Coma (,)

---

**Generado automáticamente por DIBIE Framework**  
Fecha: 2025-11-07 18:22 COT
