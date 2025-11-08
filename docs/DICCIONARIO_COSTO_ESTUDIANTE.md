# 📊 Diccionario de Datos - Costo por Estudiante/Año

## 🎯 Objetivo
Calcular con **precisión y certeza** el costo por estudiante/año en instituciones educativas.

## 📐 Fórmula Base
```
Costo_por_Estudiante = Total_Costos_Operativos / Total_Estudiantes
```

---

## ✅ Datos Actualmente Disponibles

### 1. **Matrícula** (COMPLETO ✅)
- **308 registros** de matrícula por institución y grado
- **11,798 estudiantes** totales
- **14 grados**: Prejardín, Jardín, Transición, 1° a 11°
- **4 niveles**: Preescolar, Primaria, Secundaria, Media
- **Fuente**: `hechos_matricula.csv`, `dim_grados.csv`

### 2. **Ubicación Geográfica** (COMPLETO ✅)
- 22 instituciones con coordenadas
- Datos de departamento y municipio
- **Fuente**: `ubicacion_geografica.csv`

### 3. **Ingresos** (PARCIAL ⚠️)
- Datos disponibles pero requieren normalización
- Campos actuales:
  - INGRESOS DE OPERACIÓN
  - Valor anual servicio educativo
  - INGRESOS POR OTROS COBROS
  - TOTAL INGRESOS
- **Fuente**: `hechos_financieros.csv`

---

## ❌ Datos Faltantes CRÍTICOS

### 🔴 PRIORIDAD INMEDIATA (Fase 1)

#### 1. **Costos de Personal** (60-80% del presupuesto)
- ✗ Salarios docentes (básico + prestaciones + bonificaciones)
- ✗ Salarios administrativos (rector, coordinadores, secretaria)
- ✗ Salarios servicios generales (aseo, vigilancia, cocina)
- ✗ Número de personas por categoría
- ✗ Aportes seguridad social y parafiscales

**Campos requeridos por mes:**
```
- tipo_personal (Docente/Administrativo/Servicios)
- numero_personas
- salario_promedio_mensual
- prestaciones_sociales_mes
- bonificaciones_mes
- aportes_seguridad_social_mes
- aportes_parafiscales_mes
- costo_total_mensual
```

#### 2. **Servicios Públicos**
- ✗ Energía eléctrica (mensual)
- ✗ Agua y alcantarillado (mensual)
- ✗ Gas natural (mensual, si aplica)
- ✗ Teléfono e internet (mensual)

**Campos requeridos por mes:**
```
- tipo_servicio
- proveedor
- consumo
- unidad_medida (kWh, m³, plan)
- valor_total
```

#### 3. **Servicios Contratados**
- ✗ Alimentación escolar (PAE)
- ✗ Transporte escolar
- ✗ Vigilancia y seguridad
- ✗ Servicios profesionales (contabilidad, legal)

---

### 🟡 IMPORTANTE (Fase 2 - Corto Plazo 1-2 meses)

#### 4. **Materiales y Suministros**
- ✗ Materiales didácticos y pedagógicos
- ✗ Papelería y útiles de oficina
- ✗ Productos de aseo y cafetería
- ✗ Uniformes y dotación

#### 5. **Mantenimiento**
- ✗ Mantenimiento preventivo (edificaciones, equipos)
- ✗ Mantenimiento correctivo (reparaciones)
- ✗ Adecuaciones y mejoras locativas

#### 6. **Tecnología y Equipamiento**
- ✗ Licencias de software educativo
- ✗ Equipos de cómputo
- ✗ Equipos audiovisuales y laboratorios

#### 7. **Gastos Administrativos**
- ✗ Seguros (responsabilidad civil, instalaciones)
- ✗ Impuestos prediales y tasas
- ✗ Comisiones y gastos bancarios

---

## 📋 Plantillas de Recolección

### Archivos CSV Generados (data/templates/)
1. ✅ `costos_personal.csv`
2. ✅ `servicios_publicos.csv`
3. ✅ `servicios_contratados.csv`
4. ✅ `materiales_suministros.csv`
5. ✅ `mantenimiento.csv`
6. ✅ `gastos_administrativos.csv`

### Hojas de Google Sheets
Todas las plantillas están disponibles en:
[**Google Sheets - maestro__dibie**](https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc)

Con prefijo `PLANTILLA_*`:
- PLANTILLA_costos_personal
- PLANTILLA_servicios_publicos
- PLANTILLA_servicios_contratados
- PLANTILLA_materiales
- PLANTILLA_mantenimiento
- PLANTILLA_gastos_admin

---

## 📊 Métricas Calculables

Una vez recolectados los datos, se podrán calcular:

### Métricas Básicas
- **Costo total operativo** = Suma de todos los costos
- **Costo por estudiante general** = Costo total / Total estudiantes
- **Costo por estudiante por grado** = Costo grado / Estudiantes grado
- **Costo por estudiante por nivel** = Costo nivel / Estudiantes nivel

### Indicadores de Eficiencia
- **Ratio estudiante/docente** = Total estudiantes / Número docentes
- **% Costo personal** = (Costo personal / Costo total) × 100
- **Costo docente por estudiante** = Salarios docentes / Total estudiantes
- **Margen operativo** = ((Ingresos - Costos) / Ingresos) × 100

### Benchmarks Colombia 2024
- Costo promedio estudiante oficial: **$5.000.000 - $8.000.000 COP/año**
- Costo promedio estudiante privado: **$8.000.000 - $25.000.000 COP/año**
- Ratio estudiante/docente recomendado: **25 estudiantes/docente**
- % Personal del presupuesto: **60% - 75%**

---

## 🚀 Plan de Implementación

### **Paso 1: Recolección Fase 1** (Inmediato - Esta semana)
1. Abrir plantillas en Google Sheets
2. Completar datos de **costos de personal** (último mes)
3. Completar datos de **servicios públicos** (últimos 3 meses)
4. Completar datos de **servicios contratados** (contratos vigentes)

### **Paso 2: Validación** (1 semana)
1. Revisar integridad de datos
2. Verificar totales y fórmulas
3. Comparar con estados financieros

### **Paso 3: Cálculo Inicial** (2 semanas)
1. Procesar datos en tablas normalizadas
2. Calcular costo por estudiante
3. Generar dashboard en Superset

### **Paso 4: Análisis y Optimización** (1 mes)
1. Identificar áreas de mayor costo
2. Comparar con benchmarks
3. Proponer mejoras de eficiencia

---

## 📚 Documentación Técnica

### Archivos de Referencia
- **Diccionario completo**: `data/dictionaries/diccionario_costo_por_estudiante.json`
- **Script de plantillas**: `examples/create_cost_templates.py`
- **Definiciones en Python**: `config/diccionario_costo_estudiante.py`

### Normatividad Colombia
- Ley 715 de 2001 - Sistema General de Participaciones
- Decreto 4807 de 2011 - Costos educativos
- Resolución 16432 de 2013 - Costos de matrícula y pensiones

---

## 💡 Instrucciones de Uso

### Para completar las plantillas:
1. Ir a Google Sheets: [maestro__dibie](https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc)
2. Seleccionar la hoja `PLANTILLA_*` correspondiente
3. **Eliminar filas de ejemplo** (filas 2-4)
4. Agregar datos reales de la institución
5. **NO modificar** los encabezados de columnas
6. Guardar automáticamente (Google Sheets)

### Fuentes de datos sugeridas:
- **Nómina**: Sistema de recursos humanos / Contador
- **Servicios públicos**: Facturas mensuales
- **Contratos**: Departamento administrativo
- **Compras**: Sistema de inventarios / Facturas
- **Estados financieros**: Contador / Revisor fiscal

---

## ⚠️ Validaciones Importantes

### Reglas de negocio:
- ✓ Costo total operativo > 0
- ✓ Total estudiantes > 0
- ✓ % Costo personal entre 50% y 85%
- ✓ Ratio estudiante/docente entre 15 y 35
- ✓ Margen operativo ≥ 0 (sostenibilidad)

### Alertas:
- 🚨 Si costo/estudiante < promedio × 0.7 → Revisar integridad datos
- 🚨 Si costo/estudiante > promedio × 1.5 → Revisar eficiencia
- 🚨 Si % personal > 85% → Presupuesto desbalanceado
- 🚨 Si margen < 0 → Déficit operativo

---

## 📞 Soporte

Para dudas o asistencia:
- Revisar diccionario completo en `data/dictionaries/`
- Consultar ejemplos en plantillas CSV
- Ver estructura en Google Sheets

---

**Última actualización**: 2025-11-07  
**Versión**: 1.0
