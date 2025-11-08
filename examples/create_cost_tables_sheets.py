"""
DIBIE - Crear Tablas de Costos en Google Sheets
Crear tablas estructuradas para captura de datos de costos operativos
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import time


def create_cost_tables_in_sheets():
    """
    Crear tablas de costos en Google Sheets listas para usar
    """
    print("=" * 70)
    print("DIBIE - Creación de Tablas de Costos en Google Sheets")
    print("=" * 70)
    
    # 1. Autenticar
    credentials_path = Path("config/credentials_google.json")
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # 2. Abrir spreadsheet
    print("\n1. Conectando a Google Sheets...")
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    spreadsheet = client.open_by_key(spreadsheet_id)
    print(f"   ✓ {spreadsheet.title}")
    
    # ========================================================================
    # TABLA 1: COSTOS_PERSONAL
    # ========================================================================
    print("\n2. Creando tabla: costos_personal")
    
    try:
        ws = spreadsheet.worksheet("costos_personal")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="costos_personal", rows=500, cols=15)
        print("   ✓ Hoja creada")
    
    # Encabezados
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "tipo_personal", "categoria", "numero_personas",
        "salario_promedio_mensual", "prestaciones_sociales_mes",
        "bonificaciones_mes", "aportes_seguridad_social_mes",
        "aportes_parafiscales_mes", "costo_total_mensual", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    # Formato encabezado
    ws.format('A1:N1', {
        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    # Instrucciones en nota
    ws.update_note('A1', 
        'COSTOS DE PERSONAL - Registrar mensualmente\n'
        'Tipos: Docente, Administrativo, Servicios Generales\n'
        'Categorías: Docente TC, Rector, Coordinador, Secretaria, Aseo, Vigilancia, etc.'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 2: SERVICIOS_PUBLICOS
    # ========================================================================
    print("\n3. Creando tabla: servicios_publicos")
    
    try:
        ws = spreadsheet.worksheet("servicios_publicos")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="servicios_publicos", rows=500, cols=12)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "tipo_servicio", "proveedor", "numero_factura",
        "consumo", "unidad_medida", "valor_unitario",
        "valor_total", "fecha_pago", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:M1', {
        'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.4},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'SERVICIOS PÚBLICOS - Registrar mensualmente\n'
        'Tipos: Energía Eléctrica, Agua, Gas Natural, Internet, Teléfono\n'
        'Unidades: kWh, m³, plan, etc.'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 3: SERVICIOS_CONTRATADOS
    # ========================================================================
    print("\n4. Creando tabla: servicios_contratados")
    
    try:
        ws = spreadsheet.worksheet("servicios_contratados")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="servicios_contratados", rows=500, cols=12)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "tipo_servicio", "proveedor", "numero_contrato",
        "numero_estudiantes_beneficiados", "costo_unitario_diario",
        "dias_servicio", "valor_total_mes", "fecha_pago", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:M1', {
        'backgroundColor': {'red': 0.6, 'green': 0.4, 'blue': 0.2},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'SERVICIOS CONTRATADOS - Registrar mensualmente\n'
        'Tipos: Alimentación Escolar (PAE), Transporte, Vigilancia, '
        'Servicios Profesionales (Contador, Abogado), Arrendamiento'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 4: MATERIALES_SUMINISTROS
    # ========================================================================
    print("\n5. Creando tabla: materiales_suministros")
    
    try:
        ws = spreadsheet.worksheet("materiales_suministros")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="materiales_suministros", rows=500, cols=11)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "categoria", "subcategoria", "descripcion",
        "cantidad", "valor_unitario", "valor_total",
        "fecha_compra", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:L1', {
        'backgroundColor': {'red': 0.5, 'green': 0.2, 'blue': 0.6},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'MATERIALES Y SUMINISTROS - Registrar por compra\n'
        'Categorías: Materiales Didácticos, Papelería, Aseo y Cafetería, '
        'Uniformes, Tecnología'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 5: MANTENIMIENTO
    # ========================================================================
    print("\n6. Creando tabla: mantenimiento")
    
    try:
        ws = spreadsheet.worksheet("mantenimiento")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="mantenimiento", rows=500, cols=10)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "tipo_mantenimiento", "categoria", "descripcion",
        "area_intervenida", "proveedor", "valor_total",
        "fecha_servicio", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:L1', {
        'backgroundColor': {'red': 0.7, 'green': 0.5, 'blue': 0.2},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'MANTENIMIENTO - Registrar por servicio\n'
        'Tipos: Preventivo, Correctivo, Adecuaciones\n'
        'Categorías: Edificaciones, Equipos, Mobiliario, Zonas Verdes'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 6: GASTOS_ADMINISTRATIVOS
    # ========================================================================
    print("\n7. Creando tabla: gastos_administrativos")
    
    try:
        ws = spreadsheet.worksheet("gastos_administrativos")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="gastos_administrativos", rows=500, cols=9)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "categoria", "descripcion", "proveedor",
        "valor_total", "fecha_pago", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:J1', {
        'backgroundColor': {'red': 0.3, 'green': 0.3, 'blue': 0.3},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'GASTOS ADMINISTRATIVOS - Registrar por pago\n'
        'Categorías: Seguros, Impuestos y Tasas, Publicidad, '
        'Gastos Bancarios, Honorarios Profesionales'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    time.sleep(1)
    
    # ========================================================================
    # TABLA 7: TECNOLOGIA_EQUIPAMIENTO
    # ========================================================================
    print("\n8. Creando tabla: tecnologia_equipamiento")
    
    try:
        ws = spreadsheet.worksheet("tecnologia_equipamiento")
        ws.clear()
        print("   ⚠️ Hoja existente limpiada")
    except:
        ws = spreadsheet.add_worksheet(title="tecnologia_equipamiento", rows=500, cols=10)
        print("   ✓ Hoja creada")
    
    headers = [
        "institucion_id", "dane_institucion", "anio", "mes",
        "categoria", "descripcion", "tipo_gasto",
        "cantidad", "valor_unitario", "valor_total",
        "fecha_adquisicion", "observaciones"
    ]
    
    ws.update(values=[headers], range_name='A1')
    
    ws.format('A1:L1', {
        'backgroundColor': {'red': 0.1, 'green': 0.5, 'blue': 0.8},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    ws.freeze(rows=1)
    
    ws.update_note('A1',
        'TECNOLOGÍA Y EQUIPAMIENTO - Registrar por adquisición\n'
        'Categorías: Software/Licencias, Equipos de Cómputo, '
        'Equipos Audiovisuales, Laboratorios\n'
        'Tipos: Compra, Alquiler, Licencia Anual, Licencia Mensual'
    )
    
    print(f"   ✓ Tabla lista para captura de datos")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={ws.id}")
    
    # ========================================================================
    # CREAR HOJA DE INSTRUCCIONES
    # ========================================================================
    print("\n9. Creando hoja: _INSTRUCCIONES_COSTOS")
    
    try:
        ws = spreadsheet.worksheet("_INSTRUCCIONES_COSTOS")
        ws.clear()
    except:
        ws = spreadsheet.add_worksheet(title="_INSTRUCCIONES_COSTOS", rows=100, cols=5)
    
    instrucciones = [
        ["INSTRUCCIONES PARA CAPTURA DE COSTOS OPERATIVOS"],
        [""],
        ["OBJETIVO:", "Calcular el costo por estudiante/año con precisión"],
        ["FÓRMULA:", "Costo_por_Estudiante = Total_Costos_Operativos / Total_Estudiantes"],
        [""],
        ["TABLAS DISPONIBLES:"],
        ["1. costos_personal", "Salarios, prestaciones, bonificaciones (mensual)"],
        ["2. servicios_publicos", "Energía, agua, gas, internet (mensual)"],
        ["3. servicios_contratados", "PAE, transporte, vigilancia, profesionales (mensual)"],
        ["4. materiales_suministros", "Didácticos, papelería, aseo (por compra)"],
        ["5. mantenimiento", "Preventivo, correctivo, adecuaciones (por servicio)"],
        ["6. gastos_administrativos", "Seguros, impuestos, bancarios (por pago)"],
        ["7. tecnologia_equipamiento", "Software, equipos, licencias (por adquisición)"],
        [""],
        ["PRIORIDAD DE RECOLECCIÓN:"],
        ["🔴 INMEDIATO (Fase 1):"],
        ["  • costos_personal (60-80% del presupuesto)"],
        ["  • servicios_publicos (consumo mensual)"],
        ["  • servicios_contratados (contratos vigentes)"],
        [""],
        ["🟡 CORTO PLAZO (Fase 2 - 1-2 meses):"],
        ["  • materiales_suministros"],
        ["  • mantenimiento"],
        ["  • tecnologia_equipamiento"],
        ["  • gastos_administrativos"],
        [""],
        ["INSTRUCCIONES GENERALES:"],
        ["1. NO modificar encabezados de columnas"],
        ["2. Completar todos los campos obligatorios"],
        ["3. Usar formato de fecha: YYYY-MM-DD (ej: 2024-01-15)"],
        ["4. Valores numéricos sin separadores de miles ni símbolos"],
        ["5. Registrar datos mensualmente para análisis continuo"],
        [""],
        ["CAMPOS OBLIGATORIOS EN TODAS LAS TABLAS:"],
        ["• institucion_id: Identificador de la institución"],
        ["• dane_institucion: Código DANE"],
        ["• anio: Año del registro"],
        ["• mes: Mes del registro (1-12)"],
        ["• valor_total: Valor total del costo"],
        [""],
        ["BENCHMARKS COLOMBIA 2024:"],
        ["• Costo promedio estudiante oficial: $5.000.000 - $8.000.000/año"],
        ["• Costo promedio estudiante privado: $8.000.000 - $25.000.000/año"],
        ["• % Personal del presupuesto: 60% - 75%"],
        ["• Ratio estudiante/docente: 25 estudiantes/docente"],
        [""],
        ["SOPORTE:"],
        ["• Revisar documentación en: docs/DICCIONARIO_COSTO_ESTUDIANTE.md"],
        ["• Diccionario técnico: data/dictionaries/diccionario_costo_por_estudiante.json"],
        [""],
        ["Última actualización: 2025-11-07"]
    ]
    
    ws.update(values=instrucciones, range_name='A1')
    
    # Formato
    ws.format('A1', {
        'textFormat': {'bold': True, 'fontSize': 16},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    ws.format('A3:A4', {'textFormat': {'bold': True}})
    ws.format('A6', {'textFormat': {'bold': True}})
    ws.format('A15', {'textFormat': {'bold': True}})
    ws.format('A25', {'textFormat': {'bold': True}})
    ws.format('A33', {'textFormat': {'bold': True}})
    ws.format('A39', {'textFormat': {'bold': True}})
    ws.format('A45', {'textFormat': {'bold': True}})
    
    print(f"   ✓ Hoja de instrucciones creada")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ TABLAS DE COSTOS CREADAS EXITOSAMENTE!")
    print("=" * 70)
    
    print(f"\nSpreadsheet: {spreadsheet.title}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    
    print("\n📋 TABLAS CREADAS (7):")
    print("  1. ✅ costos_personal")
    print("  2. ✅ servicios_publicos")
    print("  3. ✅ servicios_contratados")
    print("  4. ✅ materiales_suministros")
    print("  5. ✅ mantenimiento")
    print("  6. ✅ gastos_administrativos")
    print("  7. ✅ tecnologia_equipamiento")
    print("  8. ✅ _INSTRUCCIONES_COSTOS")
    
    print("\n🔴 PRIORIDAD INMEDIATA (Completar primero):")
    print("  • costos_personal")
    print("  • servicios_publicos")
    print("  • servicios_contratados")
    
    print("\n💡 SIGUIENTE PASO:")
    print("  1. Abrir el spreadsheet en Google Sheets")
    print("  2. Leer las instrucciones en '_INSTRUCCIONES_COSTOS'")
    print("  3. Empezar a completar las tablas prioritarias con datos reales")
    print("  4. Registrar datos mensualmente")
    
    print("\n✅ ¡Sistema listo para captura de datos de costos!")


if __name__ == "__main__":
    create_cost_tables_in_sheets()
