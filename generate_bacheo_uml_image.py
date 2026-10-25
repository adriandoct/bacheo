"""
Generador del Diagrama UML Gráfico de Arquitectura del Sistema de Bacheo Tijuana.
Genera una imagen PNG en ultra-alta resolución (300 DPI) para ser incrustada en Word.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon

def draw_uml_bacheo():
    fig, ax = plt.subplots(figsize=(26, 20), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 20)
    ax.axis('off')

    # Paleta de colores UML
    COLOR_STACK_HDR = '#0F766E'        # Deep Teal (Estructura de Datos Pila)
    COLOR_STACK_BG = '#F0FDFA'
    COLOR_STACK_BORDER = '#0D9488'

    COLOR_MODEL_HDR = '#1E3A8A'        # Deep Blue (Modelos MongoDB)
    COLOR_MODEL_BG = '#EFF6FF'
    COLOR_MODEL_BORDER = '#2563EB'

    COLOR_AUDIT_HDR = '#7C2D12'        # Rust/Amber (Auditoría y Secuencia)
    COLOR_AUDIT_BG = '#FFFBEB'
    COLOR_AUDIT_BORDER = '#D97706'

    COLOR_ROLE_HDR = '#4C1D95'         # Purple (Roles y Usuarios)
    COLOR_ROLE_BG = '#FAF5FF'
    COLOR_ROLE_BORDER = '#7C3AED'

    # Banner de Título
    ax.text(13.0, 19.3, "DIAGRAMA DE CLASES Y ARQUITECTURA UML: SISTEMA INTELIGENTE DE BACHEO", 
            fontsize=20, weight='bold', ha='center', va='center', color='#0F172A', fontname='DejaVu Sans')
    ax.text(13.0, 18.7, "Estructuras de Datos LIFO (Pilas) • Base de Datos MongoDB: bacheo • Roles RBAC • Tijuana, B.C.", 
            fontsize=12, style='italic', ha='center', va='center', color='#475569', fontname='DejaVu Sans')

    def draw_class_box(x, y, w, stereotype, title, subtitle, attributes, methods, header_bg, body_bg, border_color):
        header_h = 0.95
        attr_spacing = 0.26
        method_spacing = 0.25
        h_attrs = len(attributes) * attr_spacing
        h_methods = (len(methods) * method_spacing + 0.25) if methods else 0
        total_h = header_h + h_attrs + h_methods + 0.35

        # Caja principal
        box = FancyBboxPatch((x, y), w, total_h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor=body_bg, edgecolor=border_color, linewidth=1.6, zorder=2)
        ax.add_patch(box)

        # Encabezado
        hdr_box = FancyBboxPatch((x, y + total_h - header_h), w, header_h, 
                                 boxstyle="round,pad=0.02,rounding_size=0.12",
                                 facecolor=header_bg, edgecolor=border_color, linewidth=1.4, zorder=3)
        ax.add_patch(hdr_box)

        # Textos de encabezado
        ax.text(x + w/2, y + total_h - 0.22, stereotype, fontsize=7.8, weight='bold', 
                ha='center', va='center', color='#E2E8F0', fontname='DejaVu Sans', zorder=4)
        ax.text(x + w/2, y + total_h - 0.50, title, fontsize=11.5, weight='bold', 
                ha='center', va='center', color='#FFFFFF', fontname='DejaVu Sans', zorder=4)
        ax.text(x + w/2, y + total_h - 0.76, subtitle, fontsize=7.5, style='italic',
                ha='center', va='center', color='#93C5FD', fontname='DejaVu Sans', zorder=4)

        # Línea divisoria atributos
        line_y = y + total_h - header_h
        ax.plot([x, x + w], [line_y, line_y], color=border_color, linewidth=1.0, zorder=4)

        # Renderizar atributos
        cur_y = line_y - 0.20
        for attr in attributes:
            ax.text(x + 0.22, cur_y, attr, fontsize=7.5, ha='left', va='center', 
                    color='#1E293B', fontname='DejaVu Sans Mono', zorder=4)
            cur_y -= attr_spacing

        # Línea divisoria métodos
        if methods:
            ax.plot([x, x + w], [cur_y + 0.08, cur_y + 0.08], color=border_color, 
                    linewidth=0.9, linestyle='--', zorder=4)
            cur_y -= 0.16
            for meth in methods:
                ax.text(x + 0.22, cur_y, meth, fontsize=7.4, ha='left', va='center', 
                        color='#0F172A', fontname='DejaVu Sans Mono', weight='semibold', zorder=4)
                cur_y -= method_spacing

        return {'x': x, 'y': y, 'w': w, 'h': total_h, 'top': y + total_h, 'mid_y': y + total_h/2}

    # =========================================================================
    # 1. BLOQUE ESTRUCTURA DE DATOS PILAS (LIFO)
    # =========================================================================
    c_nodo = draw_class_box(
        x=1.0, y=12.2, w=5.2,
        stereotype="<<Data Structure: Node>>",
        title="NodoPila",
        subtitle="miapp.pilas.NodoPila",
        attributes=[
            "+ valor: Any (Bache)",
            "+ siguiente: Optional[NodoPila]",
        ],
        methods=[
            "+ __init__(valor, siguiente=None)",
            "+ __repr__(): str",
        ],
        header_bg=COLOR_STACK_HDR, body_bg=COLOR_STACK_BG, border_color=COLOR_STACK_BORDER
    )

    c_pila = draw_class_box(
        x=1.0, y=5.8, w=6.4,
        stereotype="<<TAD: Pila Lineal LIFO>>",
        title="Pila",
        subtitle="miapp.pilas.Pila [O(1)]",
        attributes=[
            "+ nombre: str",
            "- _tope: Optional[NodoPila]",
            "- _tamano: int = 0",
        ],
        methods=[
            "+ __init__(nombre: str)",
            "+ push(elemento: Any): void [O(1)]",
            "+ pop(): Any [O(1)]",
            "+ peek(): Any [O(1)]",
            "+ is_empty(): bool [O(1)]",
            "+ size(): int [O(1)]",
            "+ to_list(): List[Any] [O(n)]",
            "+ clear(): void",
            "+ __len__(): int",
        ],
        header_bg=COLOR_STACK_HDR, body_bg=COLOR_STACK_BG, border_color=COLOR_STACK_BORDER
    )

    c_gestor = draw_class_box(
        x=1.0, y=0.5, w=7.8,
        stereotype="<<Orquestador de Pilas de Riesgo>>",
        title="GestorPilasBacheo",
        subtitle="miapp.pilas.GestorPilasBacheo",
        attributes=[
            "+ NOMBRES_PILAS: Dict[str, str]",
            "  * 'alto': Pila Alto Riesgo (Rojo)",
            "  * 'medio': Pila Mediano Riesgo (Ámbar)",
            "  * 'bajo': Pila Bajo Riesgo (Azul)",
        ],
        methods=[
            "+ generar_codigo_bache(): str",
            "+ cargar_pila_desde_bd(nivel: str): Pila",
            "+ registrar_bache_push(datos, usuario): Tuple",
            "+ liberar_bache_pop(nivel, colaborador, ...): Tuple",
            "+ obtener_resumen_pilas(): Dict[str, Any]",
        ],
        header_bg=COLOR_STACK_HDR, body_bg=COLOR_STACK_BG, border_color=COLOR_STACK_BORDER
    )

    # =========================================================================
    # 2. BLOQUE MODELOS DE DOMINIO Y MONGODB
    # =========================================================================
    c_bache = draw_class_box(
        x=9.8, y=5.5, w=8.0,
        stereotype="<<Colección MongoDB: 'baches'>>",
        title="Bache",
        subtitle="miapp.models.Bache",
        attributes=[
            "+ id: ObjectId (PK MongoDB)",
            "+ codigo: CharField (Unique)",
            "+ ciudadano_id: FK -> Usuario (Null=True)",
            "+ nivel_riesgo: ['alto', 'medio', 'bajo']",
            "+ estado: ['pendiente', 'en_atencion', 'atendido']",
            "+ direccion: CharField (Calle y Número)",
            "+ colonia: CharField (Zona Río, Otay, etc.)",
            "+ ciudad: CharField = 'Tijuana'",
            "+ latitud: FloatField (Google Maps Lat)",
            "+ longitud: FloatField (Google Maps Lng)",
            "+ referencias: TextField",
            "+ descripcion: TextField",
            "+ diametro_estimado: CharField",
            "+ profundidad_estimada: CharField",
            "+ posicion_pila: PositiveIntegerField",
            "+ fecha_reporte: DateTimeField (Auto PUSH)",
            "+ fecha_liberacion: DateTimeField (Null POP)",
            "+ atendido_por_id: FK -> Usuario",
            "+ notas_reparacion: TextField",
            "+ material_utilizado: CharField",
            "+ tiempo_atencion_minutos: PositiveInt",
        ],
        methods=[
            "+ __str__(): str",
            "+ color_riesgo(): str",
            "+ es_atendido(): bool",
            "+ google_maps_url(): str",
            "+ google_streetview_url(): str",
        ],
        header_bg=COLOR_MODEL_HDR, body_bg=COLOR_MODEL_BG, border_color=COLOR_MODEL_BORDER
    )

    c_secuencia = draw_class_box(
        x=19.0, y=8.0, w=6.4,
        stereotype="<<Colección: 'secuencias_pila'>>",
        title="SecuenciaOperacionPila",
        subtitle="miapp.models.SecuenciaOperacionPila",
        attributes=[
            "+ id: ObjectId",
            "+ bache_id: FK -> Bache",
            "+ tipo_operacion: ['PUSH', 'POP', 'PEEK']",
            "+ pila_nombre: CharField",
            "+ usuario_id: FK -> Usuario",
            "+ rol_usuario: CharField",
            "+ fecha_hora: DateTimeField (ISO)",
            "+ posicion_en_pila: PositiveInt",
            "+ tamano_pila_antes: PositiveInt",
            "+ tamano_pila_despues: PositiveInt",
            "+ tope_codigo_previo: CharField",
            "+ tope_codigo_nuevo: CharField",
            "+ descripcion: TextField",
        ],
        methods=[
            "+ __str__(): str",
        ],
        header_bg=COLOR_AUDIT_HDR, body_bg=COLOR_AUDIT_BG, border_color=COLOR_AUDIT_BORDER
    )

    c_usuario = draw_class_box(
        x=19.0, y=0.8, w=6.4,
        stereotype="<<Colección: 'users' (RBAC)>>",
        title="Usuario",
        subtitle="miapp.models.Usuario",
        attributes=[
            "+ id: ObjectId",
            "+ user_id: 1-to-1 -> auth.User (Django)",
            "+ username: CharField",
            "+ email: EmailField",
            "+ nombre_completo: CharField",
            "+ telefono: CharField",
            "+ rol: ['admin', 'colaborador', 'ciudadano']",
            "+ activo: BooleanField = True",
            "+ creado_en: DateTimeField",
        ],
        methods=[
            "+ es_admin(): bool",
            "+ es_colaborador(): bool",
            "+ es_ciudadano(): bool",
            "+ __str__(): str",
        ],
        header_bg=COLOR_ROLE_HDR, body_bg=COLOR_ROLE_BG, border_color=COLOR_ROLE_BORDER
    )

    # =========================================================================
    # LÍNEAS DE RELACIÓN Y ASOCIACIÓN UML
    # =========================================================================
    def draw_arrow(x1, y1, x2, y2, label="", color="#334155", style='-', width=1.5):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6",
                                    color=color, lw=width, ls=style))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.15, label, fontsize=7.8, weight='bold',
                    color=color, ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=color, alpha=0.9))

    # Relación: Pila tiene NodoPila (Composición 1 -> 0..*)
    draw_arrow(3.8, c_pila['top'], 3.8, c_nodo['y'], label="1 comanda 0..* nodos (_tope)", color=COLOR_STACK_BORDER)

    # Relación: NodoPila referencia siguiente NodoPila
    ax.annotate('', xy=(6.2, c_nodo['mid_y'] + 0.3), xytext=(6.2, c_nodo['mid_y'] - 0.3),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4",
                                color=COLOR_STACK_BORDER, lw=1.3, connectionstyle="arc3,rad=-1.8"))
    ax.text(7.2, c_nodo['mid_y'], "siguiente (LIFO)", fontsize=7.2, color=COLOR_STACK_BORDER, va='center')

    # Relación: Gestor orquesta Pila (1 Gestor -> 3 Pilas de Riesgo)
    draw_arrow(4.2, c_gestor['top'], 4.2, c_pila['y'], label="Administra 3 Pilas (Alto, Medio, Bajo)", color=COLOR_STACK_BORDER)

    # Relación: Gestor persiste en Bache MongoDB
    draw_arrow(c_gestor['x'] + c_gestor['w'], c_gestor['y'] + 1.8, c_bache['x'], c_bache['y'] + 1.2, 
               label="PUSH / POP sincronizado en MongoDB", color='#059669', width=2.0)

    # Relación: SecuenciaOperacionPila registra eventos de Bache
    draw_arrow(c_bache['x'] + c_bache['w'], 11.5, c_secuencia['x'], 11.5, 
               label="Auditoría 1..* eventos", color=COLOR_AUDIT_BORDER)

    # Relación: Usuario reporta / atiende Bache
    draw_arrow(c_usuario['x'], 3.5, c_bache['x'] + c_bache['w'], 6.2, 
               label="Reporta (Ciudadano) / Atiende (Colaborador)", color=COLOR_ROLE_BORDER)

    # Cuadro de Leyenda y Explicación
    leg_box = FancyBboxPatch((10.0, 0.5), 7.8, 4.2, boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2, zorder=2)
    ax.add_patch(leg_box)
    ax.text(13.9, 4.3, "LEYENDA Y PRINCIPIOS DE DISEÑO SENIOR", fontsize=9.2, weight='bold', ha='center', color='#0F172A')
    ax.text(10.3, 3.8, "• Estructura Pila LIFO: Last-In, First-Out con inserción y extracción O(1).", fontsize=7.5, color='#334155')
    ax.text(10.3, 3.3, "• PUSH: Inserción al TOPE según nivel de riesgo (Alto, Mediano, Bajo).", fontsize=7.5, color='#0F766E')
    ax.text(10.3, 2.8, "• POP: Extracción liberada del bache en la cima al ser reparado.", fontsize=7.5, color='#B91C1C')
    ax.text(10.3, 2.3, "• PEEK: Inspección del bache prioritario sin removerlo de la estructura.", fontsize=7.5, color='#7C3AED')
    ax.text(10.3, 1.8, "• Google Maps API: Acercamiento dinámico (zoom 18) en Tijuana, B.C.", fontsize=7.5, color='#2563EB')
    ax.text(10.3, 1.3, "• Persistencia NoSQL: Base de datos MongoDB nombrada 'bacheo'.", fontsize=7.5, color='#1E3A8A')
    ax.text(10.3, 0.8, "• Control de Acceso RBAC: Admin, Colaborador (Brigada) y Ciudadano.", fontsize=7.5, color='#D97706')

    plt.tight_layout()
    output_path = "uml_sistema_bacheo_pilas.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Diagrama UML exportado exitosamente en: {output_path}")

if __name__ == "__main__":
    draw_uml_bacheo()
