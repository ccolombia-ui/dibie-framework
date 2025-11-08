"""
DIBIE - Diccionario de Datos para Costo por Estudiante/Año
Análisis de datos actuales y definición de métricas necesarias
"""

# ============================================================================
# DICCIONARIO DE DATOS - COSTO POR ESTUDIANTE/AÑO
# ============================================================================

DICCIONARIO_COSTO_ESTUDIANTE = {
    "metadata": {
        "objetivo": "Calcular con precisión el costo por estudiante/año",
        "formula_base": "Costo_por_Estudiante = Total_Costos_Operativos / Total_Estudiantes",
        "granularidad": ["Por institución", "Por año", "Por grado", "Por nivel educativo"],
        "fecha_creacion": "2025-11-07",
        "version": "1.0"
    },
    
    # ========================================================================
    # 1. DATOS DE MATRÍCULA (Ya disponibles)
    # ========================================================================
    "matricula": {
        "descripcion": "Cantidad de estudiantes por institución y grado",
        "estado": "✅ DISPONIBLE",
        "fuentes": [
            "hechos_matricula.csv (308 registros, 11,798 estudiantes)",
            "dim_grados.csv (14 grados: PJ, J, T, 1-11)"
        ],
        "campos": {
            "dane_institucion": {
                "tipo": "string",
                "descripcion": "Código DANE de la institución",
                "obligatorio": True,
                "llave_primaria": True
            },
            "anio": {
                "tipo": "integer",
                "descripcion": "Año académico",
                "obligatorio": True,
                "llave_primaria": True
            },
            "grado_codigo": {
                "tipo": "string",
                "descripcion": "Código del grado (PJ, J, T, 1-11)",
                "obligatorio": True,
                "llave_primaria": True
            },
            "cantidad_estudiantes": {
                "tipo": "integer",
                "descripcion": "Número de estudiantes matriculados",
                "obligatorio": True,
                "validacion": "cantidad_estudiantes >= 0"
            }
        },
        "metricas_calculables": [
            "Total estudiantes por institución",
            "Total estudiantes por nivel educativo",
            "Promedio estudiantes por grado"
        ]
    },
    
    # ========================================================================
    # 2. COSTOS OPERATIVOS (Parcialmente disponible - REQUIERE AMPLIACIÓN)
    # ========================================================================
    "costos_operativos": {
        "descripcion": "Costos totales de operación de la institución",
        "estado": "⚠️ PARCIAL - Requiere normalización y ampliación",
        "prioridad": "ALTA",
        
        # 2.1 COSTOS DE PERSONAL (Mayor componente - 60-80% del presupuesto)
        "personal": {
            "descripcion": "Costos relacionados con el personal",
            "estado": "❌ INCOMPLETO",
            "necesidad": "CRÍTICA",
            "campos_requeridos": {
                "salarios_docentes": {
                    "tipo": "decimal",
                    "descripcion": "Salarios totales de docentes (incluyendo prestaciones)",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "desglose": [
                        "salario_basico_docentes",
                        "prestaciones_sociales_docentes",
                        "bonificaciones_docentes",
                        "aportes_seguridad_social_docentes",
                        "aportes_parafiscales_docentes"
                    ]
                },
                "salarios_administrativos": {
                    "tipo": "decimal",
                    "descripcion": "Salarios personal administrativo",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "incluye": ["Rector", "Secretaria", "Contador", "Coordinadores"]
                },
                "salarios_servicios_generales": {
                    "tipo": "decimal",
                    "descripcion": "Salarios personal de servicios generales",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "incluye": ["Vigilancia", "Aseo", "Mantenimiento", "Cocina"]
                },
                "numero_docentes": {
                    "tipo": "integer",
                    "descripcion": "Cantidad total de docentes",
                    "obligatorio": True
                },
                "numero_administrativos": {
                    "tipo": "integer",
                    "descripcion": "Cantidad de personal administrativo",
                    "obligatorio": True
                },
                "numero_servicios_generales": {
                    "tipo": "integer",
                    "descripcion": "Cantidad de personal de servicios generales",
                    "obligatorio": True
                }
            }
        },
        
        # 2.2 SERVICIOS PÚBLICOS
        "servicios_publicos": {
            "descripcion": "Costos de servicios públicos",
            "estado": "❌ NO DISPONIBLE",
            "necesidad": "ALTA",
            "campos_requeridos": {
                "energia_electrica": {
                    "tipo": "decimal",
                    "descripcion": "Costo anual de energía eléctrica",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "frecuencia": "Mensual"
                },
                "agua_alcantarillado": {
                    "tipo": "decimal",
                    "descripcion": "Costo anual de agua y alcantarillado",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "frecuencia": "Mensual"
                },
                "gas_natural": {
                    "tipo": "decimal",
                    "descripcion": "Costo anual de gas natural (si aplica)",
                    "unidad": "pesos colombianos",
                    "obligatorio": False,
                    "frecuencia": "Mensual"
                },
                "telefono_internet": {
                    "tipo": "decimal",
                    "descripcion": "Costo anual de telefonía e internet",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "frecuencia": "Mensual"
                }
            }
        },
        
        # 2.3 MATERIALES Y SUMINISTROS
        "materiales_suministros": {
            "descripcion": "Costos de materiales educativos y suministros",
            "estado": "❌ NO DISPONIBLE",
            "necesidad": "MEDIA",
            "campos_requeridos": {
                "materiales_didacticos": {
                    "tipo": "decimal",
                    "descripcion": "Materiales didácticos y pedagógicos",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "incluye": ["Libros", "Guías", "Material audiovisual"]
                },
                "papeleria_oficina": {
                    "tipo": "decimal",
                    "descripcion": "Papelería y útiles de oficina",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "aseo_cafeteria": {
                    "tipo": "decimal",
                    "descripcion": "Productos de aseo y cafetería",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "uniformes_dotacion": {
                    "tipo": "decimal",
                    "descripcion": "Uniformes y dotación para personal",
                    "unidad": "pesos colombianos",
                    "obligatorio": False
                }
            }
        },
        
        # 2.4 MANTENIMIENTO E INFRAESTRUCTURA
        "mantenimiento": {
            "descripcion": "Costos de mantenimiento y adecuaciones",
            "estado": "❌ NO DISPONIBLE",
            "necesidad": "MEDIA",
            "campos_requeridos": {
                "mantenimiento_preventivo": {
                    "tipo": "decimal",
                    "descripcion": "Mantenimiento preventivo de instalaciones",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "incluye": ["Edificaciones", "Equipos", "Mobiliario"]
                },
                "mantenimiento_correctivo": {
                    "tipo": "decimal",
                    "descripcion": "Reparaciones y mantenimiento correctivo",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "adecuaciones_mejoras": {
                    "tipo": "decimal",
                    "descripcion": "Adecuaciones y mejoras locativas",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                }
            }
        },
        
        # 2.5 SERVICIOS CONTRATADOS
        "servicios_contratados": {
            "descripcion": "Servicios prestados por terceros",
            "estado": "⚠️ PARCIAL - Dato disponible pero sin desglose",
            "dato_actual": "Servicios generales prestados por terceros (columna en hechos_financieros)",
            "necesidad": "ALTA",
            "campos_requeridos": {
                "transporte_escolar": {
                    "tipo": "decimal",
                    "descripcion": "Costo de transporte escolar contratado",
                    "unidad": "pesos colombianos",
                    "obligatorio": False
                },
                "alimentacion_escolar": {
                    "tipo": "decimal",
                    "descripcion": "Costo de alimentación escolar (PAE)",
                    "unidad": "pesos colombianos",
                    "obligatorio": True,
                    "nota": "Puede ser subsidiado por el estado"
                },
                "vigilancia_seguridad": {
                    "tipo": "decimal",
                    "descripcion": "Servicios de vigilancia y seguridad",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "servicios_profesionales": {
                    "tipo": "decimal",
                    "descripcion": "Servicios profesionales (contabilidad, legal, etc.)",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "arrendamiento": {
                    "tipo": "decimal",
                    "descripcion": "Arrendamiento de espacios o equipos",
                    "unidad": "pesos colombianos",
                    "obligatorio": False
                }
            }
        },
        
        # 2.6 TECNOLOGÍA Y EQUIPAMIENTO
        "tecnologia": {
            "descripcion": "Costos de tecnología y equipamiento",
            "estado": "❌ NO DISPONIBLE",
            "necesidad": "MEDIA",
            "campos_requeridos": {
                "software_licencias": {
                    "tipo": "decimal",
                    "descripcion": "Licencias de software educativo",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "equipos_computo": {
                    "tipo": "decimal",
                    "descripcion": "Compra/mantenimiento de equipos de cómputo",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "equipos_audiovisuales": {
                    "tipo": "decimal",
                    "descripcion": "Equipos audiovisuales y laboratorios",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                }
            }
        },
        
        # 2.7 GASTOS ADMINISTRATIVOS
        "gastos_administrativos": {
            "descripcion": "Otros gastos administrativos",
            "estado": "❌ NO DISPONIBLE",
            "necesidad": "MEDIA",
            "campos_requeridos": {
                "seguros": {
                    "tipo": "decimal",
                    "descripcion": "Pólizas de seguros (instalaciones, responsabilidad civil)",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "impuestos_tasas": {
                    "tipo": "decimal",
                    "descripcion": "Impuestos prediales y otras tasas",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                },
                "publicidad_comunicaciones": {
                    "tipo": "decimal",
                    "descripcion": "Publicidad y comunicaciones",
                    "unidad": "pesos colombianos",
                    "obligatorio": False
                },
                "gastos_bancarios": {
                    "tipo": "decimal",
                    "descripcion": "Comisiones y gastos bancarios",
                    "unidad": "pesos colombianos",
                    "obligatorio": True
                }
            }
        }
    },
    
    # ========================================================================
    # 3. INGRESOS (Parcialmente disponible)
    # ========================================================================
    "ingresos": {
        "descripcion": "Fuentes de ingresos de la institución",
        "estado": "⚠️ PARCIAL - Requiere normalización",
        "campos_actuales": [
            "INGRESOS",
            "INGRESOS DE OPERACIÓN",
            "Valor anual servicio educativo",
            "INGRESOS POR OTROS COBROS",
            "TOTAL INGRESOS",
            "INGRESOS NO OPERACIONALES"
        ],
        "campos_requeridos": {
            "matriculas_pensiones": {
                "tipo": "decimal",
                "descripcion": "Ingresos por matrículas y pensiones",
                "unidad": "pesos colombianos",
                "obligatorio": True,
                "desglose_recomendado": ["Por grado", "Por nivel educativo"]
            },
            "transferencias_estado": {
                "tipo": "decimal",
                "descripcion": "Transferencias del Estado (SGP - Sistema General de Participaciones)",
                "unidad": "pesos colombianos",
                "obligatorio": True,
                "nota": "Para colegios oficiales"
            },
            "donaciones_aportes": {
                "tipo": "decimal",
                "descripcion": "Donaciones y aportes voluntarios",
                "unidad": "pesos colombianos",
                "obligatorio": False
            },
            "otros_ingresos": {
                "tipo": "decimal",
                "descripcion": "Otros ingresos (cafetería, eventos, etc.)",
                "unidad": "pesos colombianos",
                "obligatorio": False
            }
        }
    },
    
    # ========================================================================
    # 4. MÉTRICAS CALCULADAS
    # ========================================================================
    "metricas_calculadas": {
        "costo_total_operativo": {
            "formula": "SUM(personal + servicios_publicos + materiales + mantenimiento + servicios_contratados + tecnologia + gastos_administrativos)",
            "descripcion": "Suma de todos los costos operativos del año"
        },
        "costo_por_estudiante_general": {
            "formula": "costo_total_operativo / total_estudiantes_matriculados",
            "descripcion": "Costo promedio por estudiante en toda la institución",
            "unidad": "pesos/estudiante/año"
        },
        "costo_por_estudiante_por_grado": {
            "formula": "costo_total_operativo_grado / estudiantes_matriculados_grado",
            "descripcion": "Costo por estudiante desagregado por grado",
            "unidad": "pesos/estudiante/año",
            "nota": "Requiere distribución de costos por grado"
        },
        "costo_por_estudiante_por_nivel": {
            "formula": "costo_total_operativo_nivel / estudiantes_matriculados_nivel",
            "descripcion": "Costo por estudiante por nivel educativo (Preescolar, Primaria, Secundaria, Media)",
            "unidad": "pesos/estudiante/año"
        },
        "costo_docente_por_estudiante": {
            "formula": "salarios_docentes_totales / total_estudiantes",
            "descripcion": "Componente del costo docente por estudiante",
            "unidad": "pesos/estudiante/año"
        },
        "ratio_estudiante_docente": {
            "formula": "total_estudiantes / numero_docentes",
            "descripcion": "Número promedio de estudiantes por docente",
            "unidad": "estudiantes/docente"
        },
        "porcentaje_costo_personal": {
            "formula": "(total_costos_personal / costo_total_operativo) * 100",
            "descripcion": "Porcentaje del presupuesto destinado a personal",
            "unidad": "porcentaje"
        },
        "margen_operativo": {
            "formula": "((total_ingresos - costo_total_operativo) / total_ingresos) * 100",
            "descripcion": "Margen de rentabilidad operativa",
            "unidad": "porcentaje"
        }
    },
    
    # ========================================================================
    # 5. ESTRUCTURA DE TABLAS RECOMENDADA
    # ========================================================================
    "estructura_tablas": {
        "tabla_costos_personal": {
            "descripcion": "Costos detallados de personal",
            "campos": [
                "institucion_id", "anio", "tipo_personal", "categoria",
                "numero_personas", "salario_promedio", "costo_total",
                "prestaciones_sociales", "bonificaciones"
            ],
            "granularidad": "Por tipo de personal y año"
        },
        "tabla_costos_servicios": {
            "descripcion": "Costos de servicios públicos y contratados",
            "campos": [
                "institucion_id", "anio", "mes", "tipo_servicio",
                "proveedor", "consumo", "valor", "observaciones"
            ],
            "granularidad": "Mensual por tipo de servicio"
        },
        "tabla_costos_materiales": {
            "descripcion": "Costos de materiales y suministros",
            "campos": [
                "institucion_id", "anio", "categoria", "subcategoria",
                "descripcion", "cantidad", "valor_unitario", "valor_total"
            ],
            "granularidad": "Por categoría de material"
        },
        "tabla_costo_estudiante": {
            "descripcion": "Tabla consolidada de costo por estudiante",
            "campos": [
                "institucion_id", "anio", "grado_codigo", "nivel_educativo",
                "estudiantes_matriculados", "costo_total_asignado",
                "costo_por_estudiante", "costo_personal", "costo_operativo",
                "costo_infraestructura", "fecha_calculo"
            ],
            "granularidad": "Por institución, año y grado"
        }
    },
    
    # ========================================================================
    # 6. PLAN DE RECOLECCIÓN DE DATOS
    # ========================================================================
    "plan_recoleccion": {
        "fase_1_critica": {
            "prioridad": "INMEDIATA",
            "datos": [
                "Salarios totales de personal (docente + administrativo + servicios)",
                "Número de docentes, administrativos y personal de servicios",
                "Servicios públicos mensuales (energía, agua, internet)",
                "Servicios contratados (alimentación, vigilancia, transporte)"
            ],
            "fuentes": [
                "Nómina mensual",
                "Facturas de servicios públicos",
                "Contratos con proveedores"
            ]
        },
        "fase_2_importante": {
            "prioridad": "CORTO PLAZO (1-2 meses)",
            "datos": [
                "Materiales didácticos y suministros",
                "Mantenimiento preventivo y correctivo",
                "Tecnología y licencias de software",
                "Seguros e impuestos"
            ],
            "fuentes": [
                "Facturas de compras",
                "Órdenes de servicio de mantenimiento",
                "Contratos de licencias",
                "Declaraciones tributarias"
            ]
        },
        "fase_3_complementaria": {
            "prioridad": "MEDIANO PLAZO (3-6 meses)",
            "datos": [
                "Desglose detallado por categoría de gasto",
                "Histórico de costos (3-5 años)",
                "Proyecciones y presupuesto",
                "Benchmarking con otras instituciones"
            ],
            "fuentes": [
                "Estados financieros históricos",
                "Presupuestos aprobados",
                "Datos del sector educativo"
            ]
        }
    },
    
    # ========================================================================
    # 7. INDICADORES DE CALIDAD Y VALIDACIÓN
    # ========================================================================
    "validacion": {
        "reglas_negocio": [
            "costo_total_operativo > 0",
            "total_estudiantes > 0",
            "costo_por_estudiante = costo_total_operativo / total_estudiantes",
            "total_ingresos >= costo_total_operativo (para sostenibilidad)",
            "porcentaje_costo_personal debe estar entre 50% y 85%",
            "ratio_estudiante_docente debe estar entre 15 y 35 (según MEN Colombia)"
        ],
        "alertas": [
            "Si costo_por_estudiante < promedio_sector * 0.7: Revisar integridad de datos",
            "Si costo_por_estudiante > promedio_sector * 1.5: Revisar eficiencia operativa",
            "Si porcentaje_costo_personal > 85%: Presupuesto desbalanceado",
            "Si margen_operativo < 0: Déficit operativo - insostenible"
        ]
    },
    
    # ========================================================================
    # 8. REFERENCIAS Y BENCHMARKS
    # ========================================================================
    "referencias": {
        "fuentes_datos_colombia": [
            "SIMAT - Sistema de Matrícula",
            "SIIGO - Sistema de Información de Gestión Organizacional",
            "MEN - Ministerio de Educación Nacional",
            "ICFES - Instituto Colombiano para la Evaluación de la Educación",
            "Secretarías de Educación Departamentales/Municipales"
        ],
        "normatividad": [
            "Ley 715 de 2001 - Sistema General de Participaciones",
            "Decreto 4807 de 2011 - Costos educativos",
            "Resolución 16432 de 2013 - Costos de matrícula y pensiones"
        ],
        "benchmarks_colombia_2024": {
            "costo_promedio_estudiante_oficial": "5.000.000 - 8.000.000 COP/año",
            "costo_promedio_estudiante_privado": "8.000.000 - 25.000.000 COP/año",
            "ratio_estudiante_docente_recomendado": "25 estudiantes/docente",
            "porcentaje_personal_presupuesto": "60% - 75%"
        }
    }
}


if __name__ == "__main__":
    import json
    from pathlib import Path
    
    # Guardar diccionario
    output_dir = Path("data/dictionaries")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "diccionario_costo_por_estudiante.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(DICCIONARIO_COSTO_ESTUDIANTE, f, indent=2, ensure_ascii=False)
    
    print("=" * 70)
    print("DICCIONARIO DE DATOS - COSTO POR ESTUDIANTE/AÑO")
    print("=" * 70)
    print(f"\n✅ Guardado en: {output_file}")
    print(f"\nObjetivo: {DICCIONARIO_COSTO_ESTUDIANTE['metadata']['objetivo']}")
    print(f"Fórmula base: {DICCIONARIO_COSTO_ESTUDIANTE['metadata']['formula_base']}")
    
    # Resumen de datos disponibles vs necesarios
    print("\n" + "=" * 70)
    print("RESUMEN DE ESTADO DE DATOS")
    print("=" * 70)
    
    print("\n✅ DATOS DISPONIBLES:")
    print("   • Matrícula completa (11,798 estudiantes en 14 grados)")
    print("   • Ubicación geográfica de instituciones")
    print("   • Ingresos (parcial - requiere normalización)")
    
    print("\n⚠️ DATOS PARCIALES:")
    print("   • Costos operativos (solo algunos campos)")
    print("   • Servicios prestados por terceros (sin desglose)")
    
    print("\n❌ DATOS FALTANTES CRÍTICOS:")
    print("   • Salarios de personal (docente, administrativo, servicios)")
    print("   • Número de personal por categoría")
    print("   • Servicios públicos mensuales")
    print("   • Materiales y suministros")
    print("   • Mantenimiento e infraestructura")
    
    print("\n" + "=" * 70)
    print("PRIORIDADES DE RECOLECCIÓN")
    print("=" * 70)
    
    for fase, info in DICCIONARIO_COSTO_ESTUDIANTE['plan_recoleccion'].items():
        print(f"\n{fase.upper().replace('_', ' ')}:")
        print(f"   Prioridad: {info['prioridad']}")
        print(f"   Datos requeridos:")
        for dato in info['datos']:
            print(f"      • {dato}")
    
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASOS")
    print("=" * 70)
    print("\n1. Revisar diccionario completo en:")
    print(f"   {output_file}")
    print("\n2. Identificar fuentes de datos disponibles en la institución")
    print("\n3. Crear formularios/plantillas para recolección de datos")
    print("\n4. Implementar tablas de costos en la base de datos")
    print("\n5. Calcular métricas de costo por estudiante")
    print("\n✅ Diccionario completo generado!")
