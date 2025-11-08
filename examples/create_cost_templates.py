"""
DIBIE - Plantilla de Recolección de Datos para Costo por Estudiante
Genera archivos CSV y hojas de Google Sheets para captura de datos
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials


def create_data_collection_templates():
    """
    Crear plantillas de recolección de datos
    """
    print("=" * 70)
    print("DIBIE - Generación de Plantillas de Recolección")
    print("=" * 70)
    
    templates_dir = Path("data/templates")
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # PLANTILLA 1: COSTOS DE PERSONAL
    # ========================================================================
    print("\n1. Creando plantilla: costos_personal.csv")
    
    template_personal = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_personal": "Docente",
            "categoria": "Docente Tiempo Completo",
            "numero_personas": 15,
            "salario_promedio_mensual": 3500000,
            "prestaciones_sociales_mes": 1050000,
            "bonificaciones_mes": 200000,
            "aportes_seguridad_social_mes": 1225000,
            "aportes_parafiscales_mes": 315000,
            "costo_total_mensual": 6290000,
            "observaciones": "Incluye prima de servicios"
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_personal": "Administrativo",
            "categoria": "Rector",
            "numero_personas": 1,
            "salario_promedio_mensual": 6000000,
            "prestaciones_sociales_mes": 1800000,
            "bonificaciones_mes": 500000,
            "aportes_seguridad_social_mes": 2100000,
            "aportes_parafiscales_mes": 540000,
            "costo_total_mensual": 10940000,
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_personal": "Servicios Generales",
            "categoria": "Aseo y Mantenimiento",
            "numero_personas": 3,
            "salario_promedio_mensual": 1300000,
            "prestaciones_sociales_mes": 390000,
            "bonificaciones_mes": 0,
            "aportes_seguridad_social_mes": 455000,
            "aportes_parafiscales_mes": 117000,
            "costo_total_mensual": 2262000,
            "observaciones": ""
        }
    ])
    
    template_personal.to_csv(templates_dir / "costos_personal.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'costos_personal.csv'}")
    
    # ========================================================================
    # PLANTILLA 2: SERVICIOS PÚBLICOS
    # ========================================================================
    print("\n2. Creando plantilla: servicios_publicos.csv")
    
    template_servicios = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Energía Eléctrica",
            "proveedor": "Empresa de Energía",
            "numero_factura": "001-2024-01",
            "consumo": 5000,
            "unidad_medida": "kWh",
            "valor_unitario": 450,
            "valor_total": 2250000,
            "fecha_pago": "2024-01-15",
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Agua y Alcantarillado",
            "proveedor": "Acueducto Municipal",
            "numero_factura": "A-12345",
            "consumo": 250,
            "unidad_medida": "m³",
            "valor_unitario": 3200,
            "valor_total": 800000,
            "fecha_pago": "2024-01-20",
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Internet",
            "proveedor": "Proveedor Internet",
            "numero_factura": "INT-001",
            "consumo": 1,
            "unidad_medida": "plan",
            "valor_unitario": 350000,
            "valor_total": 350000,
            "fecha_pago": "2024-01-05",
            "observaciones": "Plan empresarial 100 Mbps"
        }
    ])
    
    template_servicios.to_csv(templates_dir / "servicios_publicos.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'servicios_publicos.csv'}")
    
    # ========================================================================
    # PLANTILLA 3: SERVICIOS CONTRATADOS
    # ========================================================================
    print("\n3. Creando plantilla: servicios_contratados.csv")
    
    template_contratados = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Alimentación Escolar (PAE)",
            "proveedor": "Operador PAE",
            "numero_contrato": "CONT-PAE-2024",
            "numero_estudiantes_beneficiados": 800,
            "costo_unitario_diario": 4500,
            "dias_servicio": 20,
            "valor_total_mes": 72000000,
            "fecha_pago": "2024-01-30",
            "observaciones": "Subsidiado por el Estado"
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Transporte Escolar",
            "proveedor": "Empresa de Transporte",
            "numero_contrato": "CONT-TRANS-2024",
            "numero_estudiantes_beneficiados": 200,
            "costo_unitario_diario": 5000,
            "dias_servicio": 20,
            "valor_total_mes": 20000000,
            "fecha_pago": "2024-01-25",
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_servicio": "Vigilancia y Seguridad",
            "proveedor": "Empresa de Vigilancia",
            "numero_contrato": "CONT-VIG-2024",
            "numero_estudiantes_beneficiados": 0,
            "costo_unitario_diario": 0,
            "dias_servicio": 30,
            "valor_total_mes": 3500000,
            "fecha_pago": "2024-01-10",
            "observaciones": "2 vigilantes 24/7"
        }
    ])
    
    template_contratados.to_csv(templates_dir / "servicios_contratados.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'servicios_contratados.csv'}")
    
    # ========================================================================
    # PLANTILLA 4: MATERIALES Y SUMINISTROS
    # ========================================================================
    print("\n4. Creando plantilla: materiales_suministros.csv")
    
    template_materiales = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "categoria": "Materiales Didácticos",
            "subcategoria": "Libros de Texto",
            "descripcion": "Libros de matemáticas grado 5",
            "cantidad": 80,
            "valor_unitario": 45000,
            "valor_total": 3600000,
            "fecha_compra": "2024-01-15",
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "categoria": "Papelería y Oficina",
            "subcategoria": "Papel",
            "descripcion": "Resmas de papel carta",
            "cantidad": 50,
            "valor_unitario": 12000,
            "valor_total": 600000,
            "fecha_compra": "2024-01-10",
            "observaciones": ""
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "categoria": "Aseo y Cafetería",
            "subcategoria": "Productos de Aseo",
            "descripcion": "Kit de limpieza mensual",
            "cantidad": 1,
            "valor_unitario": 800000,
            "valor_total": 800000,
            "fecha_compra": "2024-01-05",
            "observaciones": "Incluye jabones, desinfectantes, escobas"
        }
    ])
    
    template_materiales.to_csv(templates_dir / "materiales_suministros.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'materiales_suministros.csv'}")
    
    # ========================================================================
    # PLANTILLA 5: MANTENIMIENTO
    # ========================================================================
    print("\n5. Creando plantilla: mantenimiento.csv")
    
    template_mantenimiento = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_mantenimiento": "Preventivo",
            "categoria": "Edificaciones",
            "descripcion": "Pintura de salones de clase",
            "area_intervenida": "Bloque A - 10 salones",
            "proveedor": "Empresa de Construcción",
            "valor_total": 5000000,
            "fecha_servicio": "2024-01-20",
            "observaciones": "Mantenimiento anual programado"
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "tipo_mantenimiento": "Correctivo",
            "categoria": "Equipos",
            "descripcion": "Reparación sistema eléctrico",
            "area_intervenida": "Laboratorio de cómputo",
            "proveedor": "Electricista",
            "valor_total": 800000,
            "fecha_servicio": "2024-01-12",
            "observaciones": "Emergencia - falla en tablero"
        }
    ])
    
    template_mantenimiento.to_csv(templates_dir / "mantenimiento.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'mantenimiento.csv'}")
    
    # ========================================================================
    # PLANTILLA 6: GASTOS ADMINISTRATIVOS
    # ========================================================================
    print("\n6. Creando plantilla: gastos_administrativos.csv")
    
    template_admin = pd.DataFrame([
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "categoria": "Seguros",
            "descripcion": "Póliza de responsabilidad civil",
            "proveedor": "Aseguradora",
            "valor_total": 2500000,
            "fecha_pago": "2024-01-15",
            "observaciones": "Póliza anual prorrateada mensualmente"
        },
        {
            "institucion_id": "INST_1",
            "dane_institucion": "EJEMPLO",
            "anio": 2024,
            "mes": 1,
            "categoria": "Impuestos y Tasas",
            "descripcion": "Impuesto predial",
            "proveedor": "Municipio",
            "valor_total": 1200000,
            "fecha_pago": "2024-01-20",
            "observaciones": "Cuota trimestral"
        }
    ])
    
    template_admin.to_csv(templates_dir / "gastos_administrativos.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado: {templates_dir / 'gastos_administrativos.csv'}")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ Plantillas CSV creadas exitosamente!")
    print("=" * 70)
    
    print(f"\nUbicación: {templates_dir.absolute()}")
    print("\nArchivos generados:")
    print("  1. costos_personal.csv")
    print("  2. servicios_publicos.csv")
    print("  3. servicios_contratados.csv")
    print("  4. materiales_suministros.csv")
    print("  5. mantenimiento.csv")
    print("  6. gastos_administrativos.csv")
    
    print("\n💡 Instrucciones:")
    print("  • Cada archivo contiene filas de ejemplo")
    print("  • Eliminar filas de ejemplo antes de usar")
    print("  • Completar con datos reales de la institución")
    print("  • Mantener estructura de columnas intacta")
    
    return templates_dir


def sync_templates_to_sheets():
    """
    Sincronizar plantillas a Google Sheets
    """
    print("\n" + "=" * 70)
    print("Sincronizando plantillas con Google Sheets...")
    print("=" * 70)
    
    # Autenticar
    credentials_path = Path("config/credentials_google.json")
    
    if not credentials_path.exists():
        print("⚠️ No se encontró credentials_google.json")
        print("   Las plantillas CSV están disponibles en data/templates/")
        return
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # Abrir spreadsheet
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    spreadsheet = client.open_by_key(spreadsheet_id)
    print(f"\n✓ Conectado a: {spreadsheet.title}")
    
    # Plantillas a sincronizar
    templates_dir = Path("data/templates")
    
    templates = [
        ("costos_personal.csv", "PLANTILLA_costos_personal", "Registro mensual de costos de personal"),
        ("servicios_publicos.csv", "PLANTILLA_servicios_publicos", "Registro mensual de servicios públicos"),
        ("servicios_contratados.csv", "PLANTILLA_servicios_contratados", "Registro de servicios contratados"),
        ("materiales_suministros.csv", "PLANTILLA_materiales", "Registro de materiales y suministros"),
        ("mantenimiento.csv", "PLANTILLA_mantenimiento", "Registro de mantenimiento"),
        ("gastos_administrativos.csv", "PLANTILLA_gastos_admin", "Registro de gastos administrativos")
    ]
    
    for csv_file, sheet_name, description in templates:
        print(f"\n• Sincronizando: {sheet_name}")
        
        df = pd.read_csv(templates_dir / csv_file)
        
        # Crear o limpiar hoja
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
            print(f"  ⚠️ Hoja existente limpiada")
        except:
            worksheet = spreadsheet.add_worksheet(
                title=sheet_name,
                rows=max(100, len(df) + 50),
                cols=len(df.columns) + 2
            )
            print(f"  ✓ Hoja creada")
        
        # Escribir datos
        headers = df.columns.tolist()
        worksheet.update(values=[headers], range_name='A1')
        
        data_rows = df.astype(str).values.tolist()
        if len(data_rows) > 0:
            end_col = chr(65 + len(headers) - 1)
            worksheet.update(
                values=data_rows,
                range_name=f'A2:{end_col}{len(data_rows) + 1}'
            )
        
        # Formato
        worksheet.format('A1:ZZ1', {
            'backgroundColor': {'red': 0.8, 'green': 0.3, 'blue': 0.2},
            'textFormat': {
                'bold': True,
                'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
            },
            'horizontalAlignment': 'CENTER'
        })
        worksheet.freeze(rows=1)
        worksheet.update_note('A1', description)
        
        print(f"  ✓ {len(df)} filas de ejemplo")
        print(f"  URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={worksheet.id}")
    
    print("\n" + "=" * 70)
    print("✅ Plantillas sincronizadas con Google Sheets!")
    print("=" * 70)
    print(f"\n📊 Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")


if __name__ == "__main__":
    # Crear plantillas CSV
    templates_dir = create_data_collection_templates()
    
    # Sincronizar con Google Sheets
    sync_templates_to_sheets()
    
    print("\n" + "=" * 70)
    print("SIGUIENTE PASO: Completar las plantillas con datos reales")
    print("=" * 70)
