"""
Generador del Documento Word Oficial:
'Documentacion_Analisis_Sistema_Bacheo_Pilas.docx'
Análisis Senior Integral, Estructuras de Datos (Pilas LIFO), MongoDB, UML y Guía Paso a Paso.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def build_bacheo_docx():
    doc = docx.Document()

    # Configuración de márgenes estándar de ingeniería
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Paleta de colores ejecutiva / municipal
    COLOR_PRIMARY = RGBColor(15, 23, 42)        # #0F172A Azul marino profundo
    COLOR_SECONDARY = RGBColor(30, 58, 138)    # #1E3A8A Azul cobalto
    COLOR_CYAN = RGBColor(6, 182, 212)         # #06B6D4 Cian tecnológico
    COLOR_TEAL = RGBColor(15, 118, 110)        # #0F766E Verde azulado para Pilas
    COLOR_RED = RGBColor(185, 28, 28)          # #B91C1C Rojo de Alto Riesgo
    COLOR_AMBER = RGBColor(180, 83, 9)         # #B45309 Ámbar de Mediano Riesgo
    COLOR_TEXT = RGBColor(51, 65, 85)          # #334155 Texto grafito
    COLOR_MUTED = RGBColor(100, 116, 139)      # #64748B Gris subtítulos

    HEX_PRIMARY = "0F172A"
    HEX_SECONDARY = "1E3A8A"
    HEX_CYAN = "06B6D4"
    HEX_TEAL = "0F766E"
    HEX_RED = "B91C1C"
    HEX_AMBER = "B45309"
    HEX_BG_HEADER = "1E293B"
    HEX_BG_ALT = "F8FAFC"
    HEX_BG_CODE = "F1F5F9"
    HEX_BORDER = "CBD5E1"

    # Helpers XML de formato
    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_borders(cell, top=HEX_BORDER, bottom=HEX_BORDER, left=None, right=None, sz=4):
        tcPr = cell._tc.get_or_add_tcPr()
        borders_xml = f'<w:tcBorders {nsdecls("w")}>'
        borders_xml += f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{top}"/>' if top else '<w:top w:val="none"/>'
        borders_xml += f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{bottom}"/>' if bottom else '<w:bottom w:val="none"/>'
        borders_xml += f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{left}"/>' if left else '<w:left w:val="none"/>'
        borders_xml += f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{right}"/>' if right else '<w:right w:val="none"/>'
        borders_xml += '</w:tcBorders>'
        tcPr.append(parse_xml(borders_xml))

    def add_h1(text, icon="🔷"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run_icon = p.add_run(f"{icon} ")
        run_icon.font.size = Pt(15)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h2(text, icon="🔸"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(13)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run_icon = p.add_run(f"{icon} ")
        run_icon.font.size = Pt(12.5)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12.5)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"• {text}")
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_TEAL
        return p

    def add_p(text, bold_prefix="", italic_suffix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.bold = True
            r_bold.font.size = Pt(10)
            r_bold.font.color.rgb = COLOR_PRIMARY
        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_TEXT
        if italic_suffix:
            r_it = p.add_run(f" {italic_suffix}")
            r_it.italic = True
            r_it.font.size = Pt(9.5)
            r_it.font.color.rgb = COLOR_MUTED
        return p

    def add_callout(text, title="NOTA DE ARQUITECTURA", border_hex="06B6D4", bg_hex="F0FDFA"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=160, bottom=160, left=220, right=200)
        set_cell_borders(cell, top=None, bottom=None, left=border_hex, right=None, sz=24)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"📌 {title}: ")
        r_title.bold = True
        r_title.font.size = Pt(9.5)
        r_title.font.color.rgb = COLOR_PRIMARY
        r_body = p.add_run(text)
        r_body.font.size = Pt(9.5)
        r_body.font.color.rgb = COLOR_TEXT

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PORTADA CORPORATIVA ELEGANTE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(30)
    p_inst.paragraph_format.space_after = Pt(4)
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("H. AYUNTAMIENTO DE TIJUANA, BAJA CALIFORNIA\nDIRECCIÓN GENERAL DE OBRAS E INFRAESTRUCTURA URBANA")
    r_inst.bold = True
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = COLOR_MUTED

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(25)
    r_b = p_badge.add_run("INGENIERÍA DE SOFTWARE & ESTRUCTURAS DE DATOS AVANZADAS")
    r_b.bold = True
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = COLOR_CYAN

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("DOCUMENTACIÓN TÉCNICA Y ANÁLISIS DE ARQUITECTURA:\nSISTEMA INTELIGENTE DE BACHEO (SIT-BACHO)")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(35)
    r_sub = p_sub.add_run("Implementación de Pilas LIFO (Last-In, First-Out), Base de Datos NoSQL MongoDB ('bacheo'), Geolocalización en Google Maps y Trazabilidad Forense de Secuencias")
    r_sub.italic = True
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_TEXT

    # Tabla resumen de metadatos en portada
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Base de Datos NoSQL:", "MongoDB Enterprise (Base de Datos: 'bacheo')"),
        ("Estructura de Datos Core:", "Pilas Lineales LIFO (O(1) PUSH, POP, PEEK)"),
        ("Cobertura Geográfica:", "Tijuana, B.C. (Google Maps API + Detección a Nivel de Calle)"),
        ("Control de Acceso:", "RBAC Multinivel (Administrador, Colaborador/Cuadrilla, Ciudadano)"),
        ("Fecha de Publicación:", "Octubre 2026 • Versión 2.0 Senior Architecture"),
    ]
    for i, (k, v) in enumerate(meta_data):
        c1, c2 = meta_table.cell(i, 0), meta_table.cell(i, 1)
        c1.width, c2.width = Inches(2.5), Inches(4.2)
        set_cell_background(c1, "F1F5F9" if i % 2 == 0 else "FFFFFF")
        set_cell_background(c2, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        set_cell_margins(c2, top=100, bottom=100, left=140, right=140)
        set_cell_borders(c1, top=HEX_BORDER, bottom=HEX_BORDER)
        set_cell_borders(c2, top=HEX_BORDER, bottom=HEX_BORDER)
        
        p1 = c1.paragraphs[0]
        p1.add_run(k).bold = True
        p1.runs[0].font.size = Pt(9.5)
        p1.runs[0].font.color.rgb = COLOR_PRIMARY

        p2 = c2.paragraphs[0]
        p2.add_run(v)
        p2.runs[0].font.size = Pt(9.5)
        p2.runs[0].font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA VIAL
    # =========================================================================
    add_h1("1. INTRODUCCIÓN Y PLANTEAMIENTO DEL SISTEMA DE BACHEO", "🏙️")
    add_p(
        "El deterioro de la infraestructura vial en la ciudad de Tijuana, Baja California, representa uno de los "
        "desafíos logísticos y operativos más críticos para el gobierno municipal. Factores climáticos extraordinarios, "
        "la geografía topográfica accidentada y el intenso flujo vehicular (incluyendo transporte de carga pesada "
        "hacia garitas fronterizas) generan desprendimientos acelerados de la carpeta asfáltica. Las vialidades "
        "primarias como Paseo de los Héroes, Blvd. Agua Caliente, Vía Rápida Poniente y calzadas en Otay y Playas "
        "requieren de un esquema de respuesta altamente priorizado."
    )
    add_p(
        "Tradicionalmente, los reportes ciudadanos se acumulaban en colas desordenadas o bandejas de entrada estáticas, "
        "donde las emergencias de alto riesgo vehicular se perdían entre reportes menores. Para resolver esta problemática, "
        "se concibió el Sistema Inteligente de Bacheo (SIT-BACHO), sustentado en tres pilares arquitectónicos esenciales:",
        bold_prefix="Propósito del Sistema: "
    )
    add_p("1. Modelado de atención mediante Pilas (Stacks - LIFO) para dar respuesta contundente e inmediata al último desperfecto crítico reportado.")
    add_p("2. Integración con el API de Google Maps con capacidad de 'acercamiento dinámico' (Zoom Level 18) para la detección visual y geocodificación milimétrica del bache.")
    add_p("3. Almacenamiento NoSQL documental de alto rendimiento en MongoDB en la base de datos oficial nombrada 'bacheo', garantizando trazabilidad cronológica total de cada operación PUSH y POP.")

    add_callout(
        "A diferencia de una cola tradicional (FIFO) donde las emergencias críticas recién ingresadas deben esperar "
        "al final de una larga lista burocrática, el modelo de PILAS LIFO (Last-In, First-Out) implementado sitúa "
        "el reporte más urgente en el TOPE (cima) de la estructura operativa para su atención inmediata por las cuadrillas.",
        title="JUSTIFICACIÓN DE LA ESTRUCTURA DE PILAS"
    )

    # =========================================================================
    # SECCIÓN 2: ANÁLISIS DETALLADO DE LA ESTRUCTURA DE DATOS PILA (LIFO)
    # =========================================================================
    add_h1("2. ANÁLISIS EXHAUSTIVO DE LA ESTRUCTURA DE DATOS: PILAS (LIFO)", "📚")
    add_p(
        "Una Pila (Stack) es una estructura de datos lineal que sigue de forma estricta el principio LIFO (Last-In, First-Out). "
        "En este modelo matemático, el último elemento insertado en la cima es obligatoriamente el primer elemento en ser "
        "removido o procesado. Todas las operaciones de inserción (PUSH) y extracción (POP) se efectúan en el mismo extremo, "
        "denominado TOPE o CIMA."
    )

    add_h2("2.1. Complejidad Computacional y Rendimiento Algorítmico", "⏱️")
    add_p("La implementación desarrollada en Python sobre una lista enlazada simple garantiza eficiencia máxima:")
    
    comp_table = doc.add_table(rows=7, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Operación", "Firma del Método", "Complejidad Temporal", "Descripción Funcional"]
    for j, h in enumerate(headers):
        cell = comp_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("PUSH", "push(elemento: Any) -> None", "O(1) Constante", "Inserta el nuevo bache al tope de la pila enlazada."),
        ("POP", "pop() -> Any", "O(1) Constante", "Extrae y remueve el bache del tope al liberarse."),
        ("PEEK", "peek() -> Optional[Any]", "O(1) Constante", "Inspecciona el bache en el tope sin modificar la pila."),
        ("IS_EMPTY", "is_empty() -> bool", "O(1) Constante", "Verifica si el apuntador _tope es nulo."),
        ("SIZE", "size() -> int", "O(1) Constante", "Retorna el contador _tamano mantenido en memoria."),
        ("TO_LIST", "to_list() -> List[Any]", "O(n) Lineal", "Recorre secuencialmente desde el tope hasta la base."),
    ]
    for i, row in enumerate(comp_rows):
        for j, val in enumerate(row):
            c = comp_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if j == 0:
                p.runs[0].bold = True
            elif j == 2:
                p.runs[0].font.color.rgb = COLOR_TEAL
                p.runs[0].bold = True

    add_h2("2.2. Desglose de Clases, Constructores y Métodos", "🧩")
    
    add_h3("Clase 'NodoPila' (miapp.pilas.NodoPila)")
    add_p(
        "Representa la unidad atómica de memoria dentro de la pila. Encapsula la referencia al documento del bache "
        "y el puntero hacia el nodo subsiguiente en la jerarquía vertical.",
        bold_prefix="Función: "
    )
    add_p("• Constructor: __init__(self, valor: Any, siguiente: Optional['NodoPila'] = None)")
    add_p("  - Parámetro 'valor': Instancia del modelo Bache persistido en MongoDB.")
    add_p("  - Parámetro 'siguiente': Apuntador al nodo inferior en la pila.")

    add_h3("Clase 'Pila' (miapp.pilas.Pila)")
    add_p(
        "Implementa la estructura de datos Pila completa con encapsulamiento de estado privado.",
        bold_prefix="Función: "
    )
    add_p("• Constructor: __init__(self, nombre: str = 'Pila General')")
    add_p("  - Inicializa self.nombre con el alias de la pila.")
    add_p("  - Inicializa self._tope = None (cima vacía).")
    add_p("  - Inicializa self._tamano = 0 (contador entero).")
    add_p("• Método push(self, elemento): Crea un nuevo NodoPila asignando el nodo actual a 'siguiente' y actualiza _tope = nuevo_nodo.")
    add_p("• Método pop(self): Verifica is_empty() (lanzando PilaVaciaException si procede), extrae nodo = _tope, reasigna _tope = _tope.siguiente, decrementa _tamano y retorna el bache liberado.")
    add_p("• Método peek(self): Retorna _tope.valor de forma no destructiva.")

    add_h3("Clase 'GestorPilasBacheo' (miapp.pilas.GestorPilasBacheo)")
    add_p(
        "Patrón de diseño Fachada / Controlador que orquesta las tres pilas de criticidad vial y coordina "
        "la sincronización con la base de datos MongoDB:",
        bold_prefix="Responsabilidad: "
    )
    add_p("1. Pila de Alto Riesgo: Emergencias en vías primarias con varillas expuestas o riesgo de volcadura.")
    add_p("2. Pila de Mediano Riesgo: Bacheo preventivo y correctivo en vías con afluencia regular.")
    add_p("3. Pila de Bajo Riesgo: Reparación de agrietamientos y desgaste menor en fraccionamientos residenciales.")
    add_p("• Método registrar_bache_push(datos, usuario): Genera código único, persiste en MongoDB, ejecuta push() y crea el registro de secuencia PUSH.")
    add_p("• Método liberar_bache_pop(nivel, colaborador, notas, material): Ejecuta pop() sobre la pila indicada, marca el bache como 'atendido' en MongoDB y genera el registro de secuencia POP.")

    # =========================================================================
    # SECCIÓN 3: DIAGRAMA UML GRÁFICO Y ANÁLISIS DE ARQUITECTURA
    # =========================================================================
    add_h1("3. DIAGRAMA DE ARQUITECTURA UML Y RELACIONES", "📐")
    add_p(
        "A continuación se presenta el diagrama UML formal que modela las relaciones entre las estructuras de datos "
        "lineales en memoria (Pilas), los modelos de persistencia documental en MongoDB y los actores del sistema (RBAC):"
    )

    # Inserción de la imagen UML generada
    img_path = "uml_sistema_bacheo_pilas.png"
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap = p_cap.add_run("Figura 1: Diagrama de Clases UML del Sistema Inteligente de Bacheo (SIT-BACHO Tijuana)")
        r_cap.italic = True
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = COLOR_MUTED
    else:
        add_p("Nota: Diagrama gráfico referenciado como 'uml_sistema_bacheo_pilas.png'.")

    # =========================================================================
    # SECCIÓN 4: BASE DE DATOS NOSQL MONGODB ('bacheo')
    # =========================================================================
    add_h1("4. PERSISTENCIA EN BASE DE DATOS NOSQL: MONGODB ('bacheo')", "🍃")
    add_p(
        "El sistema almacena toda la información de manera persistente en el servidor MongoDB Server, utilizando "
        "el backend oficial 'django_mongodb_backend'. La base de datos asignada y configurada en settings.py se "
        "denomina estrictamente 'bacheo'.",
        bold_prefix="Definición de Almacenamiento: "
    )

    add_h2("4.1. Configuración en settings.py", "⚙️")
    add_p(
        "En el archivo config/settings.py se especificó la conexión directa al daemon de MongoDB:\n"
        "DATABASES = {\n"
        "    'default': {\n"
        "        'ENGINE': 'django_mongodb_backend',\n"
        "        'HOST': 'mongodb://localhost:27017/',\n"
        "        'NAME': 'bacheo',\n"
        "    }\n"
        "}"
    )

    add_h2("4.2. Estructura de las Colecciones Principales en MongoDB", "📁")
    
    col_table = doc.add_table(rows=4, cols=3)
    col_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_hdrs = ["Colección MongoDB", "Propósito en el Negocio", "Campos Relevantes / Índices BSON"]
    for j, h in enumerate(col_hdrs):
        cell = col_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    col_data = [
        ("baches", "Registro documental maestro de desperfectos viales en Tijuana.", 
         "id (_id ObjectId), codigo, nivel_riesgo ('alto', 'medio', 'bajo'), estado ('pendiente', 'atendido'), latitud, longitud, direccion, colonia, posicion_pila, fecha_reporte, fecha_liberacion, material_utilizado."),
        ("secuencias_pila", "Auditoría forense y registro cronológico de cada transición de pila.", 
         "id, bache_id, tipo_operacion ('PUSH', 'POP', 'PEEK'), pila_nombre, usuario_id, fecha_hora, tamano_pila_antes, tamano_pila_despues, tope_codigo_previo, tope_codigo_nuevo, descripcion."),
        ("users", "Cuentas de usuario y perfiles con asignación de roles operativos.", 
         "id, user_id (1-1 auth.User), username, email, nombre_completo, rol ('admin', 'colaborador', 'ciudadano'), activo."),
    ]
    for i, row in enumerate(col_data):
        for j, val in enumerate(row):
            c = col_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if j == 0:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = COLOR_SECONDARY

    # =========================================================================
    # SECCIÓN 5: INTEGRACIÓN CON GOOGLE MAPS Y GEOLOCALIZACIÓN
    # =========================================================================
    add_h1("5. INTEGRACIÓN CON GOOGLE MAPS Y DETECCIÓN EN TIJUANA", "🗺️")
    add_p(
        "El módulo de detección geográfica permite registrar de forma exacta la posición de los baches sobre la traza "
        "urbana de Tijuana, B.C., cumpliendo con el requerimiento de 'acercamiento dinámico' para inspección del asfalto:",
        bold_prefix="Mecanismo de Detección: "
    )
    add_p("• Coordenadas Centro de Tijuana: Latitud 32.5149469, Longitud -117.0382471.")
    add_p("• Detección y Acercamiento (Zoom Level 18): Al hacer clic en el mapa o ingresar una dirección (ej. 'Paseo de los Héroes, Zona Río'), el mapa ejecuta una transición animada con zoom a nivel de calle (flyTo zoom 18) permitiendo al usuario y a la brigada visualizar el carril y acotamiento exacto del desperfecto.")
    add_p("• Marcadores Cromáticos por Riesgo: Marcadores circulares con sombreado de neón: Rojo (Alto Riesgo), Ámbar (Mediano Riesgo), Azul (Bajo Riesgo) y Verde esmeralda (Atendido y Liberado).")
    add_p("• Enlace Directo a Street View: Cada marcador integra un acceso a la API de Street View en 360° para validación visual remota por los ingenieros de obras públicas.")

    # =========================================================================
    # SECCIÓN 6: GUÍA PASO A PASO PARA EXPLICACIÓN Y DEFENSA DEL SISTEMA
    # =========================================================================
    add_h1("6. GUÍA EXPLICATIVA PASO A PASO (SECUENCIA DEL SISTEMA)", "🎯")
    add_p(
        "A continuación se detalla la secuencia lógica completa para explicar el funcionamiento del sistema "
        "en una presentación académica o profesional ante directivos y evaluadores:"
    )

    steps = [
        ("PASO 1: Inicio de Sesión y Autenticación RBAC",
         "El usuario ingresa a http://127.0.0.1:8000/login/. Selecciona uno de los tres roles preconfigurados:\n"
         "• Administrador Municipal (admin / admin123)\n"
         "• Colaborador / Cuadrilla de Bacheo (colaborador / colaborador123)\n"
         "• Ciudadano Reportante (ciudadano / ciudadano123)\n"
         "El middleware de Django autentica la sesión y recupera el perfil vinculado desde MongoDB."),

        ("PASO 2: Detección Geográfica y Acercamiento en Tijuana",
         "En el portal, el usuario visualiza el mapa interactivo de Tijuana. Hace clic sobre la avenida deseada "
         "(ej. Blvd. Agua Caliente frente a Galerías Hipódromo). El sistema ejecuta un acercamiento suave a nivel de calle (zoom 18) "
         "y autocompleta la dirección, colonia y código postal mediante geocodificación inversa."),

        ("PASO 3: Ejecución de la Operación PUSH (Ingreso al Tope de la Pila)",
         "El usuario selecciona el nivel de criticidad (Alto, Mediano o Bajo Riesgo) y presiona 'Ejecutar PUSH'.\n"
         "El GestorPilasBacheo:\n"
         "1. Genera un folio único correlativo (ej. BACH-TJ-2026-0008).\n"
         "2. Inserta el nuevo nodo en la CIMA (TOPE) de la Pila de Riesgo en O(1).\n"
         "3. Guarda el documento en la colección 'baches' de MongoDB.\n"
         "4. Registra un evento 'PUSH' en 'secuencias_pila' guardando el tope previo y el nuevo tope."),

        ("PASO 4: Inspección PEEK por la Brigada Técnica",
         "El colaborador técnico ingresa a su módulo. Mediante la operación 'PEEK', el sistema examina cuál es el "
         "bache más urgente situado en la cima de la Pila de Alto Riesgo, visualizando su ubicación exacta y dimensiones "
         "sin alterar el contenido de la estructura."),

        ("PASO 5: Ejecución de la Operación POP (Atención y Liberación del Bache)",
         "Una vez que la brigada acude al sitio y repara el desperfecto con mezcla asfáltica en caliente, el colaborador "
         "hace clic en 'POP (Atender Cima)'. Se despliega el modal donde captura los materiales empleados y la bitácora técnica.\n"
         "El GestorPilasBacheo:\n"
         "1. Extrae el nodo del TOPE de la pila en O(1).\n"
         "2. Actualiza el estado en MongoDB a 'atendido', asignando la fecha de liberación y calculando el tiempo de respuesta.\n"
         "3. Registra el evento 'POP' en la colección 'secuencias_pila', promoviendo al siguiente bache como nuevo tope."),

        ("PASO 6: Generación y Consulta de Reportes de Secuencia",
         "Cualquier operador puede acceder a http://127.0.0.1:8000/reportes/secuencia/. En esta vista se visualiza el "
         "historial forense de transiciones PUSH y POP, con filtros dinámicos por operación y pila, gráficas de efectividad, "
         "y la opción de descargar el informe oficial en formato CSV para auditoría gubernamental."),
    ]

    for title_step, desc_step in steps:
        add_h2(title_step, "🔹")
        add_p(desc_step)

    # =========================================================================
    # SECCIÓN 7: MATRIZ DE ROLES Y CONTROL DE ACCESO (RBAC)
    # =========================================================================
    add_h1("7. MATRIZ DE SEGURIDAD Y CONTROL DE ACCESO (RBAC)", "🛡️")
    add_p(
        "El sistema implementa separación estricta de responsabilidades para garantizar la gobernabilidad de los datos:"
    )

    rbac_table = doc.add_table(rows=4, cols=4)
    rbac_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rbac_hdrs = ["Rol de Usuario", "Permiso PUSH (Registrar)", "Permiso POP (Liberar)", "Acceso a Reportes y Métricas"]
    for j, h in enumerate(rbac_hdrs):
        cell = rbac_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    rbac_data = [
        ("👑 Administrador Municipal", "Total (Cualquier Pila)", "Total (Cualquier Pila)", "Global (Todas las métricas y usuarios)"),
        ("🛠️ Colaborador / Brigada", "Restringido (Vía interna)", "Habilitado (Pila Asignada)", "Bitácora operativa de cuadrilla"),
        ("👤 Ciudadano de Tijuana", "Habilitado (Vía Mapa)", "Denegado (Solo lectura)", "Mis Reportes y Seguimiento en Pila"),
    ]
    for i, row in enumerate(rbac_data):
        for j, val in enumerate(row):
            c = rbac_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if j == 0:
                p.runs[0].bold = True

    # Guardado del archivo
    output_filename = "Documentacion_Analisis_Sistema_Bacheo_Pilas.docx"
    doc.save(output_filename)
    print(f"Documento Word oficial generado con éxito: {output_filename}")

if __name__ == "__main__":
    build_bacheo_docx()
