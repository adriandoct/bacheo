"""
Generador del Documento Word Oficial:
'Documentacion_MQL_Pilas_Sistema_Bacheo.docx'
Manual Técnico Exhaustivo de MongoDB Query Language (MQL),
Operaciones CRUD (Insert, Update, Delete), Estructura de Pilas (LIFO),
Recorridos y Guía Paso a Paso para Exposición y Evaluación.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def build_mql_docx():
    doc = docx.Document()

    # Configuración de márgenes estándar de ingeniería
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Paleta de colores ejecutiva / tecnológica
    COLOR_PRIMARY = RGBColor(15, 23, 42)        # #0F172A Azul marino profundo
    COLOR_SECONDARY = RGBColor(30, 58, 138)    # #1E3A8A Azul cobalto
    COLOR_GREEN_MONGO = RGBColor(16, 120, 75)  # #10784B Verde característico de MongoDB
    COLOR_CYAN = RGBColor(6, 182, 212)         # #06B6D4 Cian tecnológico
    COLOR_TEAL = RGBColor(15, 118, 110)        # #0F766E Verde azulado para Pilas
    COLOR_RED = RGBColor(185, 28, 28)          # #B91C1C Rojo de Alto Riesgo
    COLOR_AMBER = RGBColor(180, 83, 9)         # #B45309 Ámbar de Mediano Riesgo
    COLOR_TEXT = RGBColor(51, 65, 85)          # #334155 Texto grafito
    COLOR_MUTED = RGBColor(100, 116, 139)      # #64748B Gris subtítulos

    HEX_PRIMARY = "0F172A"
    HEX_SECONDARY = "1E3A8A"
    HEX_MONGO = "10AA50"
    HEX_CYAN = "06B6D4"
    HEX_TEAL = "0F766E"
    HEX_RED = "B91C1C"
    HEX_AMBER = "B45309"
    HEX_BG_HEADER = "1E293B"
    HEX_BG_ALT = "F8FAFC"
    HEX_BG_CODE = "F1F5F9"
    HEX_BORDER = "CBD5E1"
    HEX_BORDER_CODE = "94A3B8"

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
        set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
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

    def add_code_box(code_str, title=None, lang="MQL (MongoDB Query Language)"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, "0F172A")  # Fondo oscuro elegante para código
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="334155"/>'
            f'<w:left w:val="single" w:sz="20" w:space="0" w:color="10AA50"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="334155"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="334155"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1

        if title:
            r_title = p.add_run(f"⚡ {title} [{lang}]\n")
            r_title.font.name = "Consolas"
            r_title.font.size = Pt(9)
            r_title.font.bold = True
            r_title.font.color.rgb = RGBColor(16, 185, 129)  # Verde esmeralda

        r_code = p.add_run(code_str)
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(8.5)
        r_code.font.color.rgb = RGBColor(241, 245, 249)  # Blanco grisáceo

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PORTADA CORPORATIVA ELEGANTE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(25)
    p_inst.paragraph_format.space_after = Pt(4)
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SISTEMA INTELIGENTE DE GESTIÓN DE BACHEO VIAL (TIJUANA, B.C.)\nINGENIERÍA DE SOFTWARE & BASES DE DATOS NOSQL AVANZADAS")
    r_inst.bold = True
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = COLOR_MUTED

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(20)
    r_b = p_badge.add_run("GUÍA DE CONSULTAS MQL, ESTRUCTURAS LIFO Y MANUAL DE EXPOSICIÓN")
    r_b.bold = True
    r_b.font.size = Pt(10)
    r_b.font.color.rgb = COLOR_GREEN_MONGO

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("MANUAL INTEGRAL DE MQL (MONGODB QUERY LANGUAGE)\nY ANÁLISIS DE ESTRUCTURAS DE PILAS (LIFO)")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(30)
    r_sub = p_sub.add_run("Desglose minucioso de operaciones CRUD (Inserción, Modificación, Borrado), recorrido algorítmico de la pila, auditoría de secuencias y equivalencias ORM Django vs MongoDB Shell")
    r_sub.italic = True
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = COLOR_TEXT

    # Tabla resumen de metadatos en portada
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Base de Datos NoSQL:", "MongoDB Enterprise / Community (Nombre de la BD: 'bacheo')"),
        ("Lenguaje de Consultas:", "MQL (MongoDB Query Language) nativo BSON/JSON"),
        ("Conector Backend:", "django_mongodb_backend v6.0+ sobre motor Django ORM"),
        ("Estructura de Datos:", "Pilas Lineales LIFO (O(1) PUSH, POP, PEEK)"),
        ("Colecciones Principales:", "'baches', 'secuencias_pila', 'users'"),
        ("Fecha y Versión:", "Octubre 2026 • Versión 2.0 Documentación Senior"),
    ]
    for i, (k, v) in enumerate(meta_data):
        c1, c2 = meta_table.cell(i, 0), meta_table.cell(i, 1)
        c1.width, c2.width = Inches(2.5), Inches(4.3)
        set_cell_background(c1, "F1F5F9" if i % 2 == 0 else "FFFFFF")
        set_cell_background(c2, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_margins(c1, top=90, bottom=90, left=140, right=140)
        set_cell_margins(c2, top=90, bottom=90, left=140, right=140)
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
    # SECCIÓN 1: FUNDAMENTOS DE MQL Y ARQUITECTURA DE DATOS
    # =========================================================================
    add_h1("1. FUNDAMENTOS DE MQL Y ARQUITECTURA DEL SISTEMA", "🍃")
    add_p(
        "MQL (MongoDB Query Language) es el lenguaje nativo y declarativo que utiliza MongoDB para interactuar "
        "con sus bases de datos documentales. A diferencia del lenguaje SQL tradicional basado en tablas, filas "
        "y esquemas rígidos, MQL opera directamente sobre documentos en formato BSON (Binary JSON), proporcionando "
        "alta flexibilidad estructural, almacenamiento jerárquico y un rendimiento óptimo en lecturas y escrituras masivas."
    )
    add_p(
        "En este sistema de bacheo para la ciudad de Tijuana, B.C., la aplicación web desarrollada en Django se conecta "
        "a MongoDB mediante el adaptador oficial 'django_mongodb_backend'. La base de datos asignada se llama 'bacheo' "
        "(configurada en config/settings.py). Todas las instrucciones escritas en el ORM de Django (como .create(), "
        ".filter(), .save()) son traducidas internamente por el motor a sentencias nativas MQL que se ejecutan directamente "
        "en el servidor de MongoDB.",
        bold_prefix="Mapeo ORM hacia MQL: "
    )

    add_callout(
        "La base de datos del sistema está configurada en settings.py bajo la clave DATABASES['default']['NAME'] = 'bacheo', "
        "apuntando al host 'mongodb://localhost:27017/'. El enrutador 'django_mongodb_backend.routers.MongoRouter' asegura que "
        "las entidades se almacenen en colecciones BSON optimizadas para operaciones atómicas.",
        title="CONFIGURACIÓN OFICIAL DEL MOTOR"
    )

    add_h2("1.1. Colecciones Principales en MongoDB ('bacheo')", "📂")
    add_p("El sistema organiza su información en tres colecciones clave:")

    cols_table = doc.add_table(rows=4, cols=3)
    cols_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_headers = ["Colección MongoDB", "Propósito en el Negocio", "Campos Críticos"]
    for j, h in enumerate(col_headers):
        cell = cols_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    col_data = [
        ("baches", "Almacena los reportes de baches con georreferenciación en Tijuana, estado de atención y nivel de riesgo.", "_id, codigo, nivel_riesgo, estado, direccion, latitud, longitud, posicion_pila, fecha_reporte"),
        ("secuencias_pila", "Bitácora forense de auditoría que registra cada operación PUSH, POP y PEEK en las pilas.", "_id, bache_id, tipo_operacion, pila_nombre, tamano_pila_antes, tamano_pila_despues, tope_codigo_nuevo"),
        ("users", "Cuentas de usuarios y perfiles clasificados por rol (Administrador, Colaborador/Cuadrilla, Ciudadano).", "_id, username, email, rol, direccion_envio, direccion_facturacion, creado_en"),
    ]
    for i, row in enumerate(col_data):
        for j, val in enumerate(row):
            c = cols_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if j == 0:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = COLOR_GREEN_MONGO

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 2: INSERCIÓN DE INFORMACIÓN (CREATE / OPERACIÓN PUSH)
    # =========================================================================
    add_h1("2. INSERCIÓN DE INFORMACIÓN EN MQL (OPERACIÓN PUSH / CREATE)", "📥")
    add_p(
        "La inserción ocurre cuando un ciudadano o administrador reporta un nuevo bache a través de la interfaz web o API. "
        "Al ejecutarse la operación algorítmica PUSH en la pila correspondiente, se originan dos inserciones simultáneas "
        "en MongoDB: una en la colección 'baches' y otra en 'secuencias_pila' para garantizar trazabilidad forense."
    )

    add_h2("2.1. Ubicación en el Código Fuente", "📍")
    add_p("• Controlador Vista: miapp/views.py -> registrar_bache_push_view(request) (Líneas 119-189)")
    add_p("• Modelo Algorítmico: miapp/pilas.py -> GestorPilasBacheo.registrar_bache_push(datos, usuario) (Líneas 156-234)")
    add_p("• Modelo de Datos: miapp/models.py -> Bache (Líneas 391-507) y SecuenciaOperacionPila (Líneas 509-585)")

    add_h2("2.2. Sentencia Equivalente en Django ORM (Python)", "🐍")
    add_code_box(
        "# Creación atómica del bache en la cima de la pila\n"
        "nuevo_bache = Bache.objects.create(\n"
        "    codigo='BACH-TJ-2026-0004',\n"
        "    ciudadano=usuario_operador,\n"
        "    nivel_riesgo='alto',\n"
        "    estado='pendiente',\n"
        "    direccion='Paseo de los Héroes 9500',\n"
        "    colonia='Zona Urbana Río',\n"
        "    ciudad='Tijuana',\n"
        "    codigo_postal='22000',\n"
        "    latitud=32.5149469,\n"
        "    longitud=-117.0382471,\n"
        "    descripcion='Bache profundo en carril de alta velocidad',\n"
        "    diametro_estimado='75 cm',\n"
        "    profundidad_estimada='15 cm',\n"
        "    pila_tipo='alto',\n"
        "    posicion_pila=4\n"
        ")\n"
        "\n"
        "# Registro automático de auditoría PUSH\n"
        "secuencia = SecuenciaOperacionPila.objects.create(\n"
        "    bache=nuevo_bache,\n"
        "    tipo_operacion='PUSH',\n"
        "    pila_nombre='Pila de Alto Riesgo (Emergencia Vial)',\n"
        "    usuario=usuario_operador,\n"
        "    rol_usuario='ciudadano',\n"
        "    posicion_en_pila=4,\n"
        "    tamano_pila_antes=3,\n"
        "    tamano_pila_despues=4,\n"
        "    tope_codigo_previo='BACH-TJ-2026-0003',\n"
        "    tope_codigo_nuevo='BACH-TJ-2026-0004',\n"
        "    descripcion='OPERACIÓN PUSH: Registro exitoso en la cima de la pila.'\n"
        ")",
        title="Inserción vía Django ORM (miapp/pilas.py)",
        lang="Python / Django ORM"
    )

    add_h2("2.3. Sentencia Nativa en MQL (MongoDB Shell)", "💻")
    add_p("A continuación se muestra el comando exacto en MQL que se ejecuta en el servidor de MongoDB para registrar este bache:")

    add_code_box(
        "// Inserción en la colección 'baches'\n"
        "db.baches.insertOne({\n"
        "  codigo: \"BACH-TJ-2026-0004\",\n"
        "  ciudadano_id: ObjectId(\"671829a1b4e2f1001a45c001\"),\n"
        "  nivel_riesgo: \"alto\",\n"
        "  estado: \"pendiente\",\n"
        "  direccion: \"Paseo de los Héroes 9500\",\n"
        "  colonia: \"Zona Urbana Río\",\n"
        "  ciudad: \"Tijuana\",\n"
        "  codigo_postal: \"22000\",\n"
        "  latitud: 32.5149469,\n"
        "  longitud: -117.0382471,\n"
        "  referencias: \"Frente a Glorieta Cuauhtémoc\",\n"
        "  descripcion: \"Bache profundo en carril de alta velocidad\",\n"
        "  diametro_estimado: \"75 cm\",\n"
        "  profundidad_estimada: \"15 cm\",\n"
        "  foto_url: \"/static/img/bache_ejemplo.jpg\",\n"
        "  pila_tipo: \"alto\",\n"
        "  posicion_pila: 4,\n"
        "  fecha_reporte: ISODate(\"2026-10-22T16:30:00Z\"),\n"
        "  fecha_liberacion: null,\n"
        "  atendido_por_id: null,\n"
        "  notas_reparacion: \"\",\n"
        "  material_utilizado: \"Mezcla Asfáltica en Caliente y Polímero\",\n"
        "  tiempo_atencion_minutos: 0\n"
        "});\n"
        "\n"
        "// Inserción atómica en 'secuencias_pila'\n"
        "db.secuencias_pila.insertOne({\n"
        "  bache_id: ObjectId(\"671829a1b4e2f1001a45c002\"),\n"
        "  tipo_operacion: \"PUSH\",\n"
        "  pila_nombre: \"Pila de Alto Riesgo (Emergencia Vial)\",\n"
        "  usuario_id: ObjectId(\"671829a1b4e2f1001a45c001\"),\n"
        "  rol_usuario: \"ciudadano\",\n"
        "  fecha_hora: ISODate(\"2026-10-22T16:30:00Z\"),\n"
        "  posicion_en_pila: 4,\n"
        "  tamano_pila_antes: 3,\n"
        "  tamano_pila_despues: 4,\n"
        "  tope_codigo_previo: \"BACH-TJ-2026-0003\",\n"
        "  tope_codigo_nuevo: \"BACH-TJ-2026-0004\",\n"
        "  descripcion: \"OPERACIÓN PUSH: Registro exitoso del bache BACH-TJ-2026-0004 en la cima de la pila.\"\n"
        "});",
        title="MQL insertOne() sobre 'baches' y 'secuencias_pila'",
        lang="MQL Nativo"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 3: MODIFICACIÓN DE INFORMACIÓN (UPDATE / OPERACIÓN POP)
    # =========================================================================
    add_h1("3. MODIFICACIÓN DE INFORMACIÓN EN MQL (OPERACIÓN POP / UPDATE)", "🔄")
    add_p(
        "La modificación ocurre cuando una cuadrilla colaboradora atiende el bache situado en el TOPE de la pila. "
        "En la teoría de estructuras de datos, la operación POP extrae el elemento superior. En MongoDB, el documento "
        "no se destruye, sino que experimenta una mutación atómica: su estado cambia de 'pendiente' a 'atendido', se registra "
        "la marca de tiempo exacta de liberación, la cuadrilla responsable, el material asfáltico y el tiempo de respuesta."
    )

    add_h2("3.1. Ubicación en el Código Fuente", "📍")
    add_p("• Controlador Vista: miapp/views.py -> liberar_bache_pop_view(request) (Líneas 193-241)")
    add_p("• Modelo Algorítmico: miapp/pilas.py -> GestorPilasBacheo.liberar_bache_pop(...) (Líneas 236-315)")

    add_h2("3.2. Sentencia Equivalente en Django ORM (Python)", "🐍")
    add_code_box(
        "# Mutación del estado del bache en la base de datos\n"
        "bache_a_liberar.estado = 'atendido'\n"
        "bache_a_liberar.fecha_liberacion = timezone.now()\n"
        "bache_a_liberar.atendido_por = colaborador_usuario\n"
        "bache_a_liberar.notas_reparacion = 'Bache compactado con mezcla caliente y sellador polimérico.'\n"
        "bache_a_liberar.material_utilizado = 'Mezcla Asfáltica en Caliente'\n"
        "bache_a_liberar.tiempo_atencion_minutos = 45\n"
        "bache_a_liberar.save()\n"
        "\n"
        "# Registro del evento POP en auditoría\n"
        "SecuenciaOperacionPila.objects.create(\n"
        "    bache=bache_a_liberar,\n"
        "    tipo_operacion='POP',\n"
        "    pila_nombre='Pila de Alto Riesgo (Emergencia Vial)',\n"
        "    usuario=colaborador_usuario,\n"
        "    rol_usuario='colaborador',\n"
        "    posicion_en_pila=1,\n"
        "    tamano_pila_antes=4,\n"
        "    tamano_pila_despues=3,\n"
        "    tope_codigo_previo='BACH-TJ-2026-0004',\n"
        "    tope_codigo_nuevo='BACH-TJ-2026-0003',\n"
        "    descripcion='OPERACIÓN POP: Bache atendido y liberado exitosamente.'\n"
        ")",
        title="Actualización vía Django ORM (miapp/pilas.py)",
        lang="Python / Django ORM"
    )

    add_h2("3.3. Sentencia Nativa en MQL (MongoDB Shell)", "💻")
    add_p("En MQL nativo se utiliza el operador de actualización atómica '$set' mediante 'updateOne':")

    add_code_box(
        "// Actualización atómica en la colección 'baches'\n"
        "db.baches.updateOne(\n"
        "  { \n"
        "    _id: ObjectId(\"671829a1b4e2f1001a45c002\"),\n"
        "    estado: \"pendiente\" \n"
        "  },\n"
        "  {\n"
        "    $set: {\n"
        "      estado: \"atendido\",\n"
        "      fecha_liberacion: ISODate(\"2026-10-22T17:15:00Z\"),\n"
        "      atendido_por_id: ObjectId(\"671829a1b4e2f1001a45c005\"), // ID Cuadrilla\n"
        "      notas_reparacion: \"Bache compactado con mezcla caliente y sellador polimérico.\",\n"
        "      material_utilizado: \"Mezcla Asfáltica en Caliente\",\n"
        "      tiempo_atencion_minutos: 45\n"
        "    }\n"
        "  }\n"
        ");\n"
        "\n"
        "// Inserción de la auditoría de extracción (POP)\n"
        "db.secuencias_pila.insertOne({\n"
        "  bache_id: ObjectId(\"671829a1b4e2f1001a45c002\"),\n"
        "  tipo_operacion: \"POP\",\n"
        "  pila_nombre: \"Pila de Alto Riesgo (Emergencia Vial)\",\n"
        "  usuario_id: ObjectId(\"671829a1b4e2f1001a45c005\"),\n"
        "  rol_usuario: \"colaborador\",\n"
        "  fecha_hora: ISODate(\"2026-10-22T17:15:00Z\"),\n"
        "  posicion_en_pila: 1,\n"
        "  tamano_pila_antes: 4,\n"
        "  tamano_pila_despues: 3,\n"
        "  tope_codigo_previo: \"BACH-TJ-2026-0004\",\n"
        "  tope_codigo_nuevo: \"BACH-TJ-2026-0003\",\n"
        "  descripcion: \"OPERACIÓN POP: Bache BACH-TJ-2026-0004 reparado y liberado de la pila.\"\n"
        "});",
        title="MQL updateOne() con operador $set",
        lang="MQL Nativo"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 4: BORRADO DE INFORMACIÓN (DELETE VS BORRADO LÓGICO)
    # =========================================================================
    add_h1("4. BORRADO DE INFORMACIÓN EN MQL (DELETE VS BORRADO LÓGICO)", "🗑️")
    add_p(
        "En la arquitectura de sistemas gubernamentales y de ingeniería civil, la destrucción física de datos históricos "
        "constituye una mala práctica, ya que provocaría la pérdida de métricas de efectividad de las brigadas y auditorías "
        "de obras públicas. Por ello, el sistema prioriza el Borrado Lógico (Soft Delete) frente al Borrado Físico (Hard Delete)."
    )

    add_h2("4.1. Borrado Lógico (Cancelación por Falsa Alarma)", "🛡️")
    add_p(
        "En miapp/models.py (Línea 407), el modelo Bache define el estado 'cancelado'. Si un reporte resulta ser una falsa alarma "
        "o un duplicado, se cambia su estado a 'cancelado', lo cual lo excluye de inmediato de la pila de pendientes activa sin eliminar el documento."
    )

    add_code_box(
        "// MQL de Borrado Lógico (Soft Delete)\n"
        "db.baches.updateOne(\n"
        "  { codigo: \"BACH-TJ-2026-0004\" },\n"
        "  { \n"
        "    $set: { \n"
        "      estado: \"cancelado\",\n"
        "      notas_reparacion: \"Cancelado por reporte duplicado o inspección negativa.\"\n"
        "    } \n"
        "  }\n"
        ");",
        title="MQL Borrado Lógico (Soft Delete)",
        lang="MQL Nativo"
    )

    add_h2("4.2. Borrado Físico (Hard Delete en MQL)", "⚠️")
    add_p(
        "Si un Administrador del sistema requiere realizar una purga definitiva de registros de prueba durante fases de mantenimiento, "
        "se emplean los comandos nativos deleteOne() y deleteMany():"
    )

    add_code_box(
        "// 1. Eliminar físicamente un único documento por su código\n"
        "db.baches.deleteOne({ codigo: \"BACH-TJ-2026-0004\" });\n"
        "\n"
        "// 2. Eliminar físicamente todos los baches con estado 'cancelado'\n"
        "db.baches.deleteMany({ estado: \"cancelado\" });\n"
        "\n"
        "// 3. Eliminar registros de auditoría asociados a un bache purgado\n"
        "db.secuencias_pila.deleteMany({ tope_codigo_nuevo: \"BACH-TJ-2026-0004\" });",
        title="MQL deleteOne() y deleteMany() (Borrado Físico)",
        lang="MQL Nativo"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 5: ARQUITECTURA Y FUNCIONAMIENTO DE LAS PILAS (LIFO)
    # =========================================================================
    add_h1("5. CÓMO TRABAJAN LAS PILAS (STACK - LIFO) EN EL SISTEMA", "📚")
    add_p(
        "Una Pila (Stack) es una estructura de datos lineal y dinámica regida por el principio LIFO (Last-In, First-Out: "
        "'Último en Entrar, Primero en Salir'). En el contexto vial de Tijuana, este principio garantiza que cuando surge "
        "una emergencia crítica (ejemplo: un bache profundo recién formado en Vía Rápida), dicho reporte se posiciona "
        "de inmediato en el TOPE de atención para que las cuadrillas no tengan que esperar a desahogar reportes menores antiguos."
    )

    add_h2("5.1. Las Tres Pilas Especializadas por Criticidad", "🚦")
    add_p("El sistema mantiene tres pilas separadas para clasificar los desperfectos viales:")
    add_p("1. Pila de Alto Riesgo: Baches profundos (>10 cm) en vialidades primarias o vías rápidas con peligro inminente de accidente.")
    add_p("2. Pila de Mediano Riesgo: Desperfectos en avenidas secundarias o comerciales con daño progresivo a neumáticos.")
    add_p("3. Pila de Bajo Riesgo: Desgaste superficial o mantenimiento preventivo en calles residenciales.")

    add_h2("5.2. Mecanismo de Nodos y Punteros en Memoria", "🔗")
    add_p(
        "En el archivo miapp/pilas.py, la Pila no se implementa como un arreglo plano estático, sino mediante una estructura "
        "enlazada de nodos (NodoPila). Cada nodo contiene dos atributos:"
    )
    add_p("• valor: Instancia del modelo Bache persistido en MongoDB.")
    add_p("• siguiente: Puntero que referencia al nodo inmediatamente inferior en la pila.")

    add_callout(
        "Diagrama Conceptual del Mecanismo LIFO:\n"
        "  [ TOPE ]  ──> [ Bache #4 (Recién reportado) ]   <── Primer elemento en ser liberado (POP)\n"
        "                         │ siguiente\n"
        "                         ▼\n"
        "                [ Bache #3 (Reportado hace 1h) ]\n"
        "                         │ siguiente\n"
        "                         ▼\n"
        "                [ Bache #2 (Reportado hace 3h) ]\n"
        "                         │ siguiente\n"
        "                         ▼\n"
        "  [ BASE ]  ──> [ Bache #1 (Primer reporte) ]     <── Último elemento en ser liberado\n"
        "                         │ siguiente\n"
        "                        None (Fondo de la pila)",
        title="REPRESENTACIÓN DE NODOS Y PUNTEROS VERTICALES"
    )

    add_h2("5.3. Complejidad Computacional de las Operaciones", "⏱️")
    add_p("Gracias a la estructura de lista enlazada con apuntador exclusivo al tope, las operaciones elementales son óptimas:")

    perf_table = doc.add_table(rows=6, cols=3)
    perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    perf_headers = ["Operación de Pila", "Complejidad Temporal", "Comportamiento en Memoria / MongoDB"]
    for j, h in enumerate(perf_headers):
        cell = perf_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    perf_data = [
        ("PUSH (Apilar)", "O(1) Constante", "Crea un NodoPila, apunta su 'siguiente' al tope actual y actualiza el puntero _tope. Inserta en MongoDB."),
        ("POP (Desapilar)", "O(1) Constante", "Extrae el nodo del tope, reasigna _tope = _tope.siguiente y actualiza estado a 'atendido' en MongoDB."),
        ("PEEK (Mirar Tope)", "O(1) Constante", "Retorna _tope.valor sin alterar punteros ni remover el elemento."),
        ("IS_EMPTY (Vacía)", "O(1) Constante", "Evalúa si el puntero _tope is None."),
        ("SIZE (Tamaño)", "O(1) Constante", "Retorna la variable entera _tamano que se incrementa o decrementa en tiempo real."),
    ]
    for i, row in enumerate(perf_data):
        for j, val in enumerate(row):
            c = perf_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if j == 0:
                p.runs[0].bold = True
            elif j == 1:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = COLOR_TEAL

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 6: CÓMO SE RECORRE LA PILA (TRAVERSING)
    # =========================================================================
    add_h1("6. CÓMO SE RECORRE LA PILA (TRAVERSING EN MQL Y MEMORIA)", "🔍")
    add_p(
        "El recorrido de una pila (Traversing) consiste en visitar cada uno de sus elementos en el orden secuencial estricto "
        "desde el TOPE (cima) hasta la BASE (fondo). En este sistema existen dos formas complementarias de recorrer la pila:"
    )

    add_h2("6.1. Recorrido Directo en MongoDB mediante MQL", "💻")
    add_p(
        "Para consultar los elementos de la pila de Alto Riesgo ordenados exactamente como están apilados, se ejecuta "
        "una consulta con filtro de estado 'pendiente' y ordenamiento descendente (-1) por la posición de pila y fecha de reporte:"
    )

    add_code_box(
        "// 1. Recorrido completo de la pila desde el TOPE hasta la BASE\n"
        "db.baches.find(\n"
        "  {\n"
        "    nivel_riesgo: \"alto\",\n"
        "    estado: \"pendiente\"\n"
        "  }\n"
        ").sort({\n"
        "  posicion_pila: -1,   // -1 = Mayor a menor (Cima -> Fondo)\n"
        "  fecha_reporte: -1\n"
        "});\n"
        "\n"
        "// 2. Operación PEEK en MQL: Consultar ÚNICAMENTE el bache en el TOPE\n"
        "db.baches.find(\n"
        "  {\n"
        "    nivel_riesgo: \"alto\",\n"
        "    estado: \"pendiente\"\n"
        "  }\n"
        ").sort({ fecha_reporte: -1 }).limit(1);",
        title="MQL find() con sort() para Recorrido LIFO",
        lang="MQL Nativo"
    )

    add_h2("6.2. Recorrido Algorítmico en Memoria (Método to_list)", "🐍")
    add_p(
        "En el archivo miapp/pilas.py (Líneas 89-99), la clase Pila implementa el método to_list(), el cual itera sobre "
        "los nodos de la lista enlazada a partir del puntero inicial _tope con una complejidad lineal O(n):"
    )

    add_code_box(
        "def to_list(self) -> List[Any]:\n"
        "    \"\"\"\n"
        "    Retorna la representación secuencial de los elementos desde el TOPE hasta la BASE.\n"
        "    Complejidad algorítmica: O(n).\n"
        "    \"\"\"\n"
        "    elementos = []\n"
        "    actual = self._tope  # Paso 1: Posicionarse en la CIMA (Tope)\n"
        "    while actual is not None:  # Paso 2: Iterar mientras existan nodos inferiores\n"
        "        elementos.append(actual.valor)  # Paso 3: Extraer el bache\n"
        "        actual = actual.siguiente  # Paso 4: Desplazar puntero al nodo inferior\n"
        "    return elementos  # Retorna: [Bache#4 (Tope), Bache#3, Bache#2, Bache#1 (Base)]",
        title="Algoritmo de Recorrido de Pila en Python (miapp/pilas.py)",
        lang="Python / TAD Pila"
    )

    add_h2("6.3. Reconstrucción de la Pila desde MongoDB", "🔄")
    add_p(
        "Cuando el servidor web inicia o un usuario actualiza el Dashboard, el sistema reconstruye la pila en memoria "
        "desde MongoDB mediante el método GestorPilasBacheo.cargar_pila_desde_bd(nivel_riesgo) (Líneas 135-154):"
    )
    add_p("1. Consulta en MongoDB los baches pendientes ordenados cronológicamente desde el más ANTIGUO al más RECIENTE (Base -> Tope):")
    add_p("   db.baches.find({ nivel_riesgo: 'alto', estado: 'pendiente' }).sort({ fecha_reporte: 1 })")
    add_p("2. Itera la colección y ejecuta pila.push(bache) por cada documento.")
    add_p("3. Gracias a la propiedad LIFO, el último bache en entrar queda situado automáticamente en el TOPE de la estructura.")

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 7: TABLA MAESTRA DE EQUIVALENCIAS Y GUÍA DE EXPOSICIÓN
    # =========================================================================
    add_h1("7. TABLA MAESTRA DE EQUIVALENCIAS Y GUÍA DE EXPOSICIÓN", "🎯")
    add_p(
        "Esta sección sintetiza la correspondencia exacta entre los requerimientos de negocio, el código Python en Django, "
        "la operación de la estructura Pila y la sintaxis MQL de MongoDB para ser utilizada como referencia rápida durante una exposición o evaluación técnica."
    )

    eq_table = doc.add_table(rows=7, cols=4)
    eq_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eq_headers = ["Requerimiento de Negocio", "Función en Código Python", "Operación Pila", "Comando Nativo MQL (MongoDB)"]
    for j, h in enumerate(eq_headers):
        cell = eq_table.cell(0, j)
        set_cell_background(cell, HEX_BG_HEADER)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    eq_rows = [
        ("Registrar nuevo bache", "GestorPilasBacheo.registrar_bache_push", "PUSH (Apilar en Cima)", "db.baches.insertOne({...})"),
        ("Atender bache en cima", "GestorPilasBacheo.liberar_bache_pop", "POP (Desapilar del Tope)", "db.baches.updateOne({_id: ...}, {$set: {estado: 'atendido'}})"),
        ("Consultar bache prioritario", "pila.peek() / inspeccionar_peek_view", "PEEK (Mirar Tope)", "db.baches.find({estado: 'pendiente'}).sort({fecha_reporte: -1}).limit(1)"),
        ("Listar baches de la pila", "pila.to_list()", "Recorrido LIFO", "db.baches.find({estado: 'pendiente'}).sort({posicion_pila: -1})"),
        ("Auditar evento de pila", "SecuenciaOperacionPila.objects.create", "Bitácora Forense", "db.secuencias_pila.insertOne({...})"),
        ("Cancelar reporte erróneo", "bache.estado = 'cancelado'; bache.save()", "Borrado Lógico", "db.baches.updateOne({codigo: ...}, {$set: {estado: 'cancelado'}})"),
    ]
    for i, row in enumerate(eq_rows):
        for j, val in enumerate(row):
            c = eq_table.cell(i+1, j)
            set_cell_background(c, HEX_BG_ALT if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.add_run(val)
            p.runs[0].font.size = Pt(8)
            if j == 0:
                p.runs[0].bold = True
            elif j == 2:
                p.runs[0].font.color.rgb = COLOR_TEAL
                p.runs[0].bold = True
            elif j == 3:
                p.runs[0].font.name = "Consolas"
                p.runs[0].font.size = Pt(7.5)
                p.runs[0].font.color.rgb = COLOR_GREEN_MONGO

    add_h2("7.1. Preguntas Clave y Respuestas para Defender la Exposición", "🗣️")
    
    add_p(
        "El MQL es el lenguaje nativo con el que MongoDB gestiona sus colecciones y documentos BSON. En este proyecto, "
        "Django utiliza el conector django_mongodb_backend, lo que permite que cada instrucción del modelo (como Bache.objects.create) "
        "se traduzca a un comando nativo MQL como db.baches.insertOne() sobre la base de datos 'bacheo'.",
        bold_prefix="P1: ¿Qué es MQL y cómo se relaciona con Django en este sistema? -> "
    )
    add_p(
        "La inserción se realiza en la operación PUSH con db.baches.insertOne(), asignándole una posición de pila. "
        "La modificación ocurre en la operación POP con db.baches.updateOne() usando el operador $set para marcarlo como 'atendido'. "
        "El borrado preferido es un borrado lógico (actualizando el estado a 'cancelado'), aunque también se soportan db.baches.deleteOne() "
        "y deleteMany() para purgas físicas.",
        bold_prefix="P2: ¿Dónde inserta, modifica y borra información el sistema? -> "
    )
    add_p(
        "Trabajan bajo el principio LIFO (Last-In, First-Out). Mantenemos 3 pilas según el nivel de riesgo vial (Alto, Mediano, Bajo). "
        "En memoria se estructuran con nodos enlazados donde cada nodo apunta al siguiente inferior. Las operaciones PUSH, POP y PEEK "
        "tienen complejidad O(1) porque solo acceden al puntero del TOPE sin iterar la colección.",
        bold_prefix="P3: ¿Cómo trabajan las pilas y cuál es su complejidad algorítmica? -> "
    )
    add_p(
        "En la base de datos se recorre con db.baches.find({estado: 'pendiente'}).sort({posicion_pila: -1}), que extrae los documentos "
        "del más nuevo al más antiguo. En memoria se recorre con el método to_list() que parte del puntero _tope y navega los punteros "
        "'siguiente' de cada nodo hasta llegar a None con complejidad lineal O(n).",
        bold_prefix="P4: ¿Cómo se recorre la pila (Traversing)? -> "
    )
    add_p(
        "Se ubica en 'config/settings.py' en la constante GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'TU_CLAVE'). "
        "En MongoDB se vincula directamente con las coordenadas BSON {latitud, longitud} guardadas mediante MQL en la colección 'baches', "
        "permitiendo que el método google_maps_url() construya enlaces directos de navegación GPS para las cuadrillas en campo.",
        bold_prefix="P5: ¿Dónde se ubica la API KEY de Google Maps y cómo se enlaza con MongoDB/MQL? -> "
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 8: ANEXO - UBICACIÓN Y CONFIGURACIÓN DE LA API KEY DE GOOGLE MAPS
    # =========================================================================
    add_h1("8. ANEXO: UBICACIÓN Y CONFIGURACIÓN DE LA API KEY DE GOOGLE MAPS", "🗺️")

    add_p(
        "El Sistema Inteligente de Bacheo utiliza georreferenciación de alta precisión para ubicar cada daño vial "
        "reportado en Tijuana, Baja California. Para la integración con los servicios geoespaciales de Google "
        "(Google Maps JavaScript API, Geocoding API y Navigation URLs), el proyecto cuenta con una arquitectura "
        "centralizada, modular y segura."
    )

    add_callout(
        "Por directrices y estándares de ciberseguridad, las credenciales y llaves de acceso a APIs de terceros "
        "nunca deben quedar expuestas de forma fija en el código en repositorios públicos. El sistema implementa "
        "lectura prioritaria desde variables de entorno del sistema operativo ('GOOGLE_MAPS_API_KEY') con valor de respaldo en archivo.",
        title="BUENAS PRÁCTICAS DE SEGURIDAD EN API KEYS",
        border_hex="F59E0B",
        bg_hex="FFFBEB"
    )

    add_h2("8.1. Ubicación Exacta en el Código Fuente (config/settings.py)", "⚙️")
    add_p(
        "La clave de Google Maps se configura formalmente en el archivo principal de configuración de Django: "
        "'config/settings.py' (al final del archivo, alrededor de la línea 141):"
    )

    add_code_box(
        "# ==============================================================================\n"
        "# CONFIGURACIÓN DE API KEY DE GOOGLE MAPS & SERVICIOS GEOESPACIALES\n"
        "# ==============================================================================\n"
        "# Archivo: config/settings.py (Línea ~141)\n"
        "import os\n\n"
        "# 1. Vía Variable de Entorno (Recomendado para Producción):\n"
        "GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')\n\n"
        "# 2. O Asignación Directa para Pruebas Locales:\n"
        "# GOOGLE_MAPS_API_KEY = 'AIzaSyA_TU_CLAVE_REAL_DE_GOOGLE_MAPS_AQUI'",
        title="Definición de GOOGLE_MAPS_API_KEY en config/settings.py",
        lang="Python / Django Settings"
    )

    add_h2("8.2. Inyección en los Controladores y Vistas (miapp/views.py)", "🔌")
    add_p(
        "En el controlador 'miapp/views.py', la clave es leída dinámicamente desde settings e inyectada "
        "en el diccionario de contexto que Django envía a la interfaz gráfica del usuario:"
    )

    add_code_box(
        "# Archivo: miapp/views.py (dentro de la función index / dashboard):\n"
        "from django.conf import settings\n\n"
        "def index(request):\n"
        "    # Obtención segura de la API KEY desde la configuración central\n"
        "    google_maps_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')\n\n"
        "    context = {\n"
        "        # ... estado de pilas de riesgo, baches y auditoría ...\n"
        "        'google_maps_api_key': google_maps_api_key,\n"
        "    }\n"
        "    return render(request, 'miapp/bacheo_dashboard.html', context)",
        title="Lectura e Inyección en Controlador Django",
        lang="Python"
    )

    add_h2("8.3. Consumo en la Plantilla Frontend (miapp/templates/miapp/bacheo_dashboard.html)", "🖥️")
    add_p(
        "En la plantilla del dashboard, la API Key se recibe como variable Django '{{ google_maps_api_key }}' "
        "y se utiliza para invocar los servicios oficiales de Google Maps o resolver direcciones mediante Geocoding:"
    )

    add_code_box(
        "<!-- Invocación de la API de Google Maps en la plantilla HTML -->\n"
        "{% if google_maps_api_key %}\n"
        "  <script src=\"https://maps.googleapis.com/maps/api/js?key={{ google_maps_api_key }}&libraries=places\"></script>\n"
        "{% endif %}",
        title="Invocación en bacheo_dashboard.html",
        lang="HTML / Django Template"
    )

    add_h2("8.4. Conexión Directa entre Coordenadas BSON en MongoDB (MQL) y Google Maps", "🔗")
    add_p(
        "Cada bache almacenado en MongoDB mediante MQL guarda un subdocumento BSON con sus coordenadas geográficas exactas. "
        "El modelo 'Bache' cuenta con el método 'google_maps_url()' que traduce esas coordenadas BSON a un enlace universal de navegación:"
    )

    add_code_box(
        "// 1. Documento BSON almacenado en MongoDB mediante MQL (db.baches.insertOne):\n"
        "{\n"
        "  \"_id\": ObjectId(\"663fa89b1c9d4b001a123456\"),\n"
        "  \"codigo\": \"BACH-2026-0001\",\n"
        "  \"ubicacion\": {\n"
        "    \"latitud\": 32.5149469,\n"
        "    \"longitud\": -116.945231,\n"
        "    \"direccion_texto\": \"Av. Paseo de los Héroes 9500, Zona Urbana Río, Tijuana\"\n"
        "  },\n"
        "  \"nivel_riesgo\": \"alto\",\n"
        "  \"posicion_pila\": 1\n"
        "}\n\n"
        "// 2. Método Python en el modelo Bache (miapp/models.py):\n"
        "def google_maps_url(self):\n"
        "    lat = self.ubicacion.get('latitud', 32.5149469)\n"
        "    lng = self.ubicacion.get('longitud', -116.945231)\n"
        "    return f\"https://www.google.com/maps/search/?api=1&query={lat},{lng}\"",
        title="Correspondencia entre BSON (MQL) y Navegación Google Maps",
        lang="BSON / Python"
    )

    add_callout(
        "Ventaja Operativa: Gracias a esta correspondencia directa, las cuadrillas de obras públicas pueden "
        "desapilar un bache prioritario (operación POP) y hacer clic en el enlace 'Ver en Google Maps', abriendo "
        "de inmediato la ruta GPS óptima hacia las coordenadas guardadas en MongoDB.",
        title="VENTAJA OPERATIVA PARA CUADRILLAS EN CAMPO",
        border_hex="10AA50",
        bg_hex="F0FDF4"
    )

    output_filename = "Documentacion_MQL_Pilas_Sistema_Bacheo.docx"
    try:
        doc.save(output_filename)
        print(f"Documento generado exitosamente: {output_filename}")
    except PermissionError:
        fallback_name = "Documentacion_MQL_Pilas_Sistema_Bacheo_Actualizada.docx"
        doc.save(fallback_name)
        print(f"AVISO: {output_filename} está abierto en Word. Se guardó como: {fallback_name}")

if __name__ == "__main__":
    build_mql_docx()
