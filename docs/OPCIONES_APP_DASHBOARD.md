# 📱 Opciones para App de Captura de Datos + Dashboard Interactivo

## 🎯 Objetivo Dual
1. **App móvil/web** para captura fácil de datos de costos
2. **Dashboard interactivo** con mapa geográfico para análisis

---

## OPCIÓN 1: Google AppSheet ⭐ RECOMENDADO

### ✅ Ventajas
- **Conexión directa** con Google Sheets (ya tenemos las tablas)
- **Generación automática** de app sin código
- **Aplicación móvil** (Android/iOS) + web
- **Formularios inteligentes** con validaciones
- **Escaneo de facturas** con OCR
- **Trabajo offline** con sincronización
- **GRATIS** hasta 10 usuarios

### 📋 Cómo Generar AppSheet

#### Método 1: Desde Google Sheets (MÁS FÁCIL)
```
1. Abrir: https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc
2. Menú: Extensiones → AppSheet → Crear una app
3. AppSheet detecta automáticamente la estructura de tablas
4. Personalizar formularios y vistas
5. Publicar app
```

#### Método 2: Desde AppSheet.com
```
1. Ir a: https://www.appsheet.com
2. Iniciar sesión con cuenta Google (aksobhya-googlesheet-806@aksobhya.iam.gserviceaccount.com)
3. "Create" → "Start with your own data"
4. Conectar Google Sheets
5. Seleccionar spreadsheet: maestro__dibie
6. AppSheet genera app automáticamente
```

### 🔧 Configuración Recomendada AppSheet

**Tablas a incluir en la app:**
- ✅ costos_personal
- ✅ servicios_publicos
- ✅ servicios_contratados
- ✅ materiales_suministros
- ✅ mantenimiento
- ✅ gastos_administrativos
- ✅ tecnologia_equipamiento

**Funcionalidades sugeridas:**
- Formularios por tipo de costo
- Validación de campos obligatorios
- Cálculos automáticos (costo_total = cantidad × valor_unitario)
- Filtros por institución, mes, año
- Notificaciones de recordatorio mensual
- Captura de fotos de facturas

### 💰 Costo
- **Free**: Hasta 10 usuarios
- **Starter**: $5/usuario/mes (usuarios ilimitados)
- **Core**: $10/usuario/mes (funciones avanzadas)

---

## OPCIÓN 2: API de Google Sheets + App Custom

### 🔌 Google Sheets API v4
Podemos crear una app web custom que use la API de Google Sheets.

**Ventajas:**
- Control total del diseño
- Integración con otros servicios
- Sin límites de usuarios
- Hosting gratuito (Vercel, Netlify)

**Tecnologías sugeridas:**
- **Frontend**: Next.js 14 + Tailwind CSS
- **Backend**: Google Sheets API v4
- **Auth**: Google OAuth 2.0
- **Hosting**: Vercel (gratis)

### 📝 Código de Integración (ya disponible en Python)

Podemos adaptar nuestro código actual para crear una API REST:

```python
# API endpoint usando FastAPI
from fastapi import FastAPI
from google.oauth2.service_account import Credentials
import gspread

app = FastAPI()

@app.post("/api/costos/personal")
def create_costo_personal(data: dict):
    # Conectar a Google Sheets
    # Insertar datos
    # Retornar confirmación
    pass

@app.get("/api/costos/resumen/{institucion_id}")
def get_resumen_costos(institucion_id: str):
    # Obtener datos de todas las tablas
    # Calcular totales
    # Retornar JSON
    pass
```

---

## OPCIÓN 3: Microsoft Power Apps

### 🔌 Conexión con Google Sheets
- Requiere connector premium ($$$)
- Mejor si ya tienen licencias Microsoft 365
- Integración con Power BI para dashboards

**NO RECOMENDADO** en este caso (ya usamos Google Workspace)

---

## 📧 RECOLECCIÓN POR EMAIL

### Google Forms → Google Sheets (GRATIS)

Podemos crear formularios Google que envíen datos directamente a las hojas:

```javascript
// Script en Google Sheets para recibir emails con datos
function procesarEmailConDatos() {
  var threads = GmailApp.search('subject:"Reporte Costos" is:unread');
  
  threads.forEach(thread => {
    var messages = thread.getMessages();
    messages.forEach(message => {
      // Parsear email
      // Extraer datos
      // Insertar en hoja correspondiente
      message.markRead();
    });
  });
}
```

### Configuración:
1. Crear cuenta: `costos@dibie.edu.co` (ejemplo)
2. Google Apps Script para procesar emails
3. Plantilla de email con formato estructurado
4. Trigger automático cada hora

---

## 🗺️ DASHBOARD INTERACTIVO + MAPA

### OPCIÓN A: Apache Superset (Ya instalado) ⭐

**Ventajas:**
- Ya lo tenemos configurado
- Mapas interactivos con Deck.gl
- Filtros dinámicos
- Dashboards profesionales
- GRATIS y open source

**Dashboards a crear:**

#### 1. **Mapa de Costos por Institución**
```sql
-- Vista para el mapa
CREATE VIEW v_mapa_costos_institucion AS
SELECT 
    mi.dane_institucion,
    mi.nombre,
    mi.municipio,
    mi.departamento,
    ug.latitud,
    ug.longitud,
    SUM(COALESCE(cp.costo_total_mensual, 0)) as costo_personal,
    SUM(COALESCE(sp.valor_total, 0)) as costo_servicios,
    SUM(COALESCE(sc.valor_total_mes, 0)) as costo_contratados,
    COUNT(hm.cantidad_estudiantes) as total_estudiantes,
    (SUM(costos) / NULLIF(SUM(estudiantes), 0)) as costo_por_estudiante
FROM maestro_instituciones mi
LEFT JOIN ubicacion_geografica ug ON mi.iebm_id = ug.institucion_id
LEFT JOIN hechos_matricula hm ON mi.dane_institucion = hm.dane_institucion
-- JOINs con tablas de costos
GROUP BY mi.dane_institucion, mi.nombre, ug.latitud, ug.longitud;
```

**Visualizaciones:**
- 🗺️ Mapa de calor (costo por estudiante)
- 📊 Gráfico de barras (costos por categoría)
- 📈 Línea de tiempo (evolución mensual)
- 🥧 Pie chart (distribución de costos)
- 📋 Tabla detallada con filtros

#### 2. **Dashboard de Análisis Financiero**
- KPIs principales: Total costos, costo/estudiante, margen
- Comparativo por institución
- Tendencias mensuales
- Top 5 costos más altos

### OPCIÓN B: Looker Studio (Google Data Studio) - GRATIS

**Ventajas:**
- Conexión directa con Google Sheets
- Mapas de Google Maps integrados
- Compartir dashboards fácilmente
- 100% gratis

**Cómo crear:**
```
1. Ir a: https://lookerstudio.google.com
2. Crear → Informe
3. Agregar datos → Google Sheets
4. Seleccionar maestro__dibie
5. Arrastrar y soltar visualizaciones
```

**Visualizaciones recomendadas:**
- Mapa geográfico con marcadores por institución
- Tarjetas de métricas (total estudiantes, costos, costo/estudiante)
- Gráficos de serie temporal
- Tablas con drill-down

### OPCIÓN C: Tableau Public - GRATIS

- Muy potente para visualizaciones
- Mapas interactivos excelentes
- Limitación: datos públicos solamente
- Exportar desde Google Sheets a CSV

---

## 🎯 RECOMENDACIÓN FINAL

### Para CAPTURA DE DATOS:
**Google AppSheet** (Opción 1)
- ✅ Rápido de implementar (1-2 horas)
- ✅ App móvil nativa
- ✅ Conexión directa con Google Sheets
- ✅ Gratis para 10 usuarios
- ✅ Trabajo offline

### Para DASHBOARD + MAPA:
**Apache Superset** (ya instalado) + **Looker Studio**
- ✅ Superset: Dashboards avanzados, mapas de calor
- ✅ Looker Studio: Compartir fácilmente, mapas Google Maps
- ✅ Ambos GRATIS
- ✅ Complementarios

### Para EMAIL:
**Google Apps Script** en Google Sheets
- ✅ Automatización completa
- ✅ Gratis
- ✅ Integración nativa

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### Semana 1: App de Captura
```
Día 1-2: Configurar Google AppSheet
  - Conectar con Google Sheets
  - Generar app automáticamente
  - Personalizar formularios

Día 3-4: Pruebas y ajustes
  - Validaciones
  - Flujos de trabajo
  - Permisos de usuario

Día 5: Capacitación
  - Manual de usuario
  - Video tutorial
  - Despliegue a usuarios
```

### Semana 2: Dashboards
```
Día 1-2: Superset Dashboards
  - Crear vistas SQL
  - Diseñar dashboards
  - Configurar mapas interactivos

Día 3-4: Looker Studio
  - Conectar Google Sheets
  - Crear visualizaciones
  - Diseñar informes ejecutivos

Día 5: Integración
  - Enlazar app con dashboards
  - Pruebas end-to-end
  - Documentación
```

### Semana 3: Automatización Email
```
Día 1-2: Google Apps Script
  - Script de procesamiento de emails
  - Plantillas de email
  - Triggers automáticos

Día 3-4: Pruebas
  - Envío de emails de prueba
  - Validación de datos
  - Manejo de errores

Día 5: Producción
  - Activar automatización
  - Monitoreo
  - Soporte
```

---

## 📊 COMPARATIVA RÁPIDA

| Característica | AppSheet | Custom App | Looker Studio | Superset |
|----------------|----------|------------|---------------|----------|
| Costo | Gratis | Gratis | Gratis | Gratis |
| Tiempo setup | 2 horas | 2 semanas | 1 día | 2 días |
| App móvil | ✅ Sí | ⚠️ PWA | ❌ No | ❌ No |
| Mapas | ⚠️ Básico | ✅ Custom | ✅ Google Maps | ✅ Deck.gl |
| Offline | ✅ Sí | ⚠️ Depende | ❌ No | ❌ No |
| Código | ❌ No-code | ✅ Full code | ❌ No-code | ⚠️ SQL |
| Curva aprendizaje | Baja | Alta | Baja | Media |

---

## 💡 DECISIÓN

**Para empezar HOY:**
1. ✅ **Google AppSheet** para captura de datos
2. ✅ **Looker Studio** para dashboards compartibles
3. ✅ **Apache Superset** para análisis avanzado

**Para el futuro:**
- Si necesitan más control → Desarrollar app custom
- Si crecen > 10 usuarios → Upgrade AppSheet
- Si necesitan análisis complejo → Potenciar Superset

---

¿Quieres que genere la app de AppSheet ahora o prefieres que empiece con los dashboards en Superset/Looker Studio?
