"""
Vistas del Sistema Inteligente de Bacheo (Tijuana, B.C.)
=========================================================
Controladores con estructuras de control empresariales para la gestión
de pilas (LIFO), geolocalización con Google Maps, reportes de secuencia
y autenticación por roles (Admin, Colaborador, Ciudadano) sobre MongoDB.
"""

import json
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.utils import timezone

from .models import Usuario, Bache, SecuenciaOperacionPila
from .pilas import GestorPilasBacheo, PilaVaciaException, BacheInvalidoException


def get_user_role(user):
    """
    Determina de forma precisa el rol del usuario actual:
    'admin'        -> Administrador de Obras Públicas
    'colaborador'  -> Cuadrilla técnica que atiende y libera baches
    'ciudadano'    -> Usuario que reporta y consulta estado
    """
    if not user or not user.is_authenticated:
        return 'ciudadano'
    if user.is_superuser:
        return 'admin'
    perfil = getattr(user, 'perfil', None)
    if perfil:
        if perfil.rol in ['admin', 'colaborador', 'ciudadano']:
            return perfil.rol
    if user.groups.filter(name='Administradores').exists():
        return 'admin'
    if user.groups.filter(name='Colaboradores').exists() or 'colabora' in user.username.lower():
        return 'colaborador'
    return 'ciudadano'


def get_perfil_usuario(user):
    """Obtiene o vincula el perfil Usuario correspondiente a un auth.User."""
    if not user or not user.is_authenticated:
        return None
    perfil, _ = Usuario.objects.get_or_create(
        user=user,
        defaults={
            'username': user.username,
            'email': user.email or f"{user.username}@tijuana.gob.mx",
            'nombre_completo': user.get_full_name() or user.username.title(),
            'rol': 'admin' if user.is_superuser else 'ciudadano',
        }
    )
    return perfil


# ==============================================================================
# DASHBOARD PRINCIPAL Y VISTAS DE ROL
# ==============================================================================

@login_required(login_url='login')
def index(request):
    """
    Vista principal adaptable del Sistema Inteligente de Bacheo.
    Se adapta al rol actual (Admin, Colaborador, Ciudadano) presentando:
    - Estado de las 3 Pilas de Riesgo (Alto, Mediano, Bajo)
    - Mapa de Tijuana interactivo con Google Maps
    - Módulo de operaciones PUSH (Registro) y POP (Liberación)
    - Trazabilidad y métricas de desempeño
    """
    user_role = get_user_role(request.user)
    perfil = get_perfil_usuario(request.user)

    # Cargar estado analítico de las tres pilas (LIFO)
    resumen_pilas = GestorPilasBacheo.obtener_resumen_pilas()

    # Todos los baches para renderizado en mapa
    baches_todos = Bache.objects.all().order_by('-fecha_reporte')
    baches_pendientes = Bache.objects.filter(estado='pendiente').order_by('-posicion_pila', '-fecha_reporte')
    baches_atendidos = Bache.objects.filter(estado='atendido').order_by('-fecha_liberacion')

    # Baches específicos para el Ciudadano
    mis_reportes = []
    if user_role == 'ciudadano' and perfil:
        mis_reportes = Bache.objects.filter(ciudadano=perfil).order_by('-fecha_reporte')
    elif user_role == 'colaborador' and perfil:
        mis_reportes = Bache.objects.filter(atendido_por=perfil).order_by('-fecha_liberacion')

    # Llave de Google Maps (desde settings o env)
    google_maps_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')

    context = {
        'db_name': settings.DATABASES['default']['NAME'],
        'user_role': user_role,
        'perfil': perfil,
        'resumen_pilas': resumen_pilas,
        'baches_pendientes': baches_pendientes[:20],
        'baches_atendidos': baches_atendidos[:10],
        'baches_todos_count': baches_todos.count(),
        'mis_reportes': mis_reportes,
        'google_maps_api_key': google_maps_api_key,
        'ahora': timezone.now(),
    }
    return render(request, 'miapp/bacheo_dashboard.html', context)


# ==============================================================================
# OPERACIONES DE PILA: PUSH (REGISTRO) Y POP (LIBERACIÓN / ATENCIÓN)
# ==============================================================================

@login_required(login_url='login')
@require_POST
def registrar_bache_push_view(request):
    """
    Operación PUSH sobre la Pila correspondiente de riesgo (Alto, Mediano o Bajo).
    Inserta un nuevo bache geolocalizado en Tijuana y actualiza la cima de la pila.
    """
    perfil = get_perfil_usuario(request.user)

    direccion = request.POST.get('direccion', '').strip()
    colonia = request.POST.get('colonia', 'Zona Río').strip()
    codigo_postal = request.POST.get('codigo_postal', '22000').strip()
    nivel_riesgo = request.POST.get('nivel_riesgo', 'medio').strip().lower()
    descripcion = request.POST.get('descripcion', '').strip()
    referencias = request.POST.get('referencias', '').strip()
    diametro = request.POST.get('diametro_estimado', '60 cm').strip()
    profundidad = request.POST.get('profundidad_estimada', '12 cm').strip()
    foto_url = request.POST.get('foto_url', '').strip()

    # Coordenadas geográficas con fallback seguro en Tijuana
    try:
        latitud = float(request.POST.get('latitud', 32.5149469))
        longitud = float(request.POST.get('longitud', -117.0382471))
    except (ValueError, TypeError):
        latitud = 32.5149469
        longitud = -117.0382471

    # Estructura de control: Validaciones de integridad
    if not direccion:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'La dirección en Tijuana es obligatoria.'}, status=400)
        messages.error(request, "Error: Debes especificar la dirección o hacer clic en el mapa de Tijuana.")
        return redirect('index')

    datos_bache = {
        'direccion': direccion,
        'colonia': colonia,
        'codigo_postal': codigo_postal,
        'latitud': latitud,
        'longitud': longitud,
        'nivel_riesgo': nivel_riesgo,
        'descripcion': descripcion or f"Reporte de bache en {direccion}, {colonia}",
        'referencias': referencias,
        'diametro_estimado': diametro,
        'profundidad_estimada': profundidad,
        'foto_url': foto_url,
    }

    try:
        nuevo_bache, secuencia = GestorPilasBacheo.registrar_bache_push(
            datos=datos_bache,
            usuario_operador=perfil
        )
        msg_exito = f"Operación PUSH exitosa: Bache {nuevo_bache.codigo} registrado en el TOPE de la Pila de {nuevo_bache.get_nivel_riesgo_display()}."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'message': msg_exito,
                'codigo': nuevo_bache.codigo,
                'nivel_riesgo': nuevo_bache.nivel_riesgo,
                'posicion': nuevo_bache.posicion_pila,
            })

        messages.success(request, msg_exito)
    except Exception as e:
        msg_err = f"Error al ejecutar operación PUSH: {str(e)}"
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': msg_err}, status=500)
        messages.error(request, msg_err)

    return redirect('index')


@login_required(login_url='login')
@require_POST
def liberar_bache_pop_view(request):
    """
    Operación POP sobre la Pila de riesgo seleccionada.
    Atiende el bache en el TOPE de la pila, lo marca como atendido y lo libera.
    Exclusivo para Colaboradores y Administradores.
    """
    user_role = get_user_role(request.user)
    if user_role not in ['admin', 'colaborador']:
        messages.error(request, "Acceso restringido: Solo las cuadrillas colaboradoras o administradores pueden liberar baches de la pila.")
        return redirect('index')

    perfil = get_perfil_usuario(request.user)
    nivel_riesgo = request.POST.get('nivel_riesgo', 'alto').strip().lower()
    bache_id = request.POST.get('bache_id', '').strip() or None
    notas = request.POST.get('notas_reparacion', '').strip()
    material = request.POST.get('material_utilizado', 'Mezcla Asfáltica Caliente con Polímero').strip()

    try:
        bache_liberado, secuencia = GestorPilasBacheo.liberar_bache_pop(
            nivel_riesgo=nivel_riesgo,
            colaborador_usuario=perfil,
            notas_reparacion=notas,
            material_utilizado=material,
            bache_especifico_id=bache_id
        )

        msg_exito = f"Operación POP exitosa: Bache {bache_liberado.codigo} atendido y liberado de la {secuencia.pila_nombre}. Nuevo tope: {secuencia.tope_codigo_nuevo}."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'message': msg_exito,
                'codigo': bache_liberado.codigo,
                'tope_nuevo': secuencia.tope_codigo_nuevo,
                'tamano_despues': secuencia.tamano_pila_despues,
            })

        messages.success(request, msg_exito)
    except PilaVaciaException as pve:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'empty', 'message': str(pve)}, status=400)
        messages.warning(request, str(pve))
    except Exception as e:
        msg_err = f"Error al procesar operación POP: {str(e)}"
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': msg_err}, status=500)
        messages.error(request, msg_err)

    return redirect('index')


@login_required(login_url='login')
@require_GET
def inspeccionar_peek_view(request, nivel_riesgo):
    """
    Operación PEEK: Inspecciona el elemento en la cima de la pila sin extraerlo.
    """
    nivel = nivel_riesgo.lower()
    pila = GestorPilasBacheo.cargar_pila_desde_bd(nivel)
    tope = pila.peek()

    if not tope:
        return JsonResponse({
            'status': 'empty',
            'mensaje': f'La pila de {nivel} riesgo se encuentra vacía.',
            'tamano': 0,
        })

    return JsonResponse({
        'status': 'ok',
        'pila': pila.nombre,
        'tamano': pila.size(),
        'tope': {
            'id': str(tope.id),
            'codigo': tope.codigo,
            'direccion': tope.direccion,
            'colonia': tope.colonia,
            'nivel_riesgo': tope.nivel_riesgo,
            'descripcion': tope.descripcion,
            'latitud': tope.latitud,
            'longitud': tope.longitud,
            'fecha_reporte': tope.fecha_reporte.strftime('%Y-%m-%d %H:%M'),
        }
    })


# ==============================================================================
# REPORTES DE SECUENCIA Y AUDITORÍA DE PROCESOS
# ==============================================================================

@login_required(login_url='login')
def reportes_secuencia_view(request):
    """
    Vista de auditoría y análisis de secuencias de procesos:
    Reporte cronológico de todas las operaciones PUSH y POP ejecutadas,
    con filtros interactivos, métricas de respuesta y visualización de flujo.
    """
    user_role = get_user_role(request.user)
    perfil = get_perfil_usuario(request.user)

    # Filtros
    operacion_filtro = request.GET.get('operacion', '').strip().upper()
    pila_filtro = request.GET.get('pila', '').strip()
    busqueda = request.GET.get('q', '').strip()

    secuencias_qs = SecuenciaOperacionPila.objects.select_related('bache', 'usuario').all()

    if operacion_filtro in ['PUSH', 'POP', 'PEEK']:
        secuencias_qs = secuencias_qs.filter(tipo_operacion=operacion_filtro)
    if pila_filtro:
        secuencias_qs = secuencias_qs.filter(pila_nombre__icontains=pila_filtro)
    if busqueda:
        secuencias_qs = secuencias_qs.filter(
            bache__codigo__icontains=busqueda
        ) | secuencias_qs.filter(
            descripcion__icontains=busqueda
        ) | secuencias_qs.filter(
            usuario__nombre_completo__icontains=busqueda
        )

    # Métricas estadísticas
    total_push = SecuenciaOperacionPila.objects.filter(tipo_operacion='PUSH').count()
    total_pop = SecuenciaOperacionPila.objects.filter(tipo_operacion='POP').count()
    total_pendientes = Bache.objects.filter(estado='pendiente').count()
    total_atendidos = Bache.objects.filter(estado='atendido').count()

    context = {
        'secuencias': secuencias_qs[:100],
        'total_push': total_push,
        'total_pop': total_pop,
        'total_pendientes': total_pendientes,
        'total_atendidos': total_atendidos,
        'operacion_filtro': operacion_filtro,
        'pila_filtro': pila_filtro,
        'busqueda': busqueda,
        'user_role': user_role,
        'perfil': perfil,
    }
    return render(request, 'miapp/reportes_secuencia.html', context)


@login_required(login_url='login')
def exportar_reporte_csv(request):
    """Exporta la secuencia de procesos (PUSH / POP) en formato CSV."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="secuencia_bacheo_tijuana.csv"'
    response.write('\ufeff')  # BOM para Excel en español

    writer = csv.writer(response)
    writer.writerow([
        'ID Secuencia',
        'Operación Pila',
        'Pila Afectada',
        'Código Bache',
        'Dirección Tijuana',
        'Colonia',
        'Nivel Riesgo',
        'Usuario Operador',
        'Rol',
        'Fecha y Hora',
        'Tamaño Pila Antes',
        'Tamaño Pila Después',
        'Tope Código Previo',
        'Tope Código Nuevo',
        'Detalle Evento',
    ])

    secuencias = SecuenciaOperacionPila.objects.select_related('bache', 'usuario').all()
    for s in secuencias:
        b = s.bache
        writer.writerow([
            str(s.id),
            s.tipo_operacion,
            s.pila_nombre,
            b.codigo if b else '',
            b.direccion if b else '',
            b.colonia if b else '',
            b.get_nivel_riesgo_display() if b else '',
            s.usuario.nombre_completo if s.usuario else 'Sistema',
            s.rol_usuario,
            s.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            s.tamano_pila_antes,
            s.tamano_pila_despues,
            s.tope_codigo_previo,
            s.tope_codigo_nuevo,
            s.descripcion,
        ])

    return response


# ==============================================================================
# ENDPOINTS API PARA GOOGLE MAPS Y ACTUALIZACIÓN ASÍNCRONA
# ==============================================================================

@login_required(login_url='login')
@require_GET
def api_baches_puntos(request):
    """
    Retorna la colección completa de puntos de baches en Tijuana
    con coordenadas geográficas, nivel de riesgo, estado y detalles
    para renderizado dinámico en Google Maps.
    """
    baches = Bache.objects.all().order_by('-fecha_reporte')
    features = []

    for b in baches:
        features.append({
            'id': str(b.id),
            'codigo': b.codigo,
            'direccion': b.direccion,
            'colonia': b.colonia,
            'nivel_riesgo': b.nivel_riesgo,
            'nivel_riesgo_display': b.get_nivel_riesgo_display(),
            'color': b.color_riesgo,
            'estado': b.estado,
            'estado_display': b.get_estado_display(),
            'latitud': b.latitud,
            'longitud': b.longitud,
            'descripcion': b.descripcion,
            'diametro': b.diametro_estimado,
            'profundidad': b.profundidad_estimada,
            'posicion_pila': b.posicion_pila,
            'fecha_reporte': b.fecha_reporte.strftime('%d/%m/%Y %H:%M'),
            'fecha_liberacion': b.fecha_liberacion.strftime('%d/%m/%Y %H:%M') if b.fecha_liberacion else None,
            'atendido_por': b.atendido_por.nombre_completo if b.atendido_por else None,
            'notas_reparacion': b.notas_reparacion,
            'material': b.material_utilizado,
            'google_maps_url': b.google_maps_url(),
            'google_streetview_url': b.google_streetview_url(),
        })

    return JsonResponse({'status': 'ok', 'count': len(features), 'baches': features})


@login_required(login_url='login')
@require_GET
def api_pilas_estado(request):
    """Retorna en JSON el estado actual de las 3 pilas para actualización reactiva en UI."""
    resumen = GestorPilasBacheo.obtener_resumen_pilas()

    def serialize_pila(pila_data):
        return {
            'nombre': pila_data['nombre'],
            'tamano': pila_data['tamano'],
            'tope': {
                'id': str(pila_data['tope'].id),
                'codigo': pila_data['tope'].codigo,
                'direccion': pila_data['tope'].direccion,
                'colonia': pila_data['tope'].colonia,
                'latitud': pila_data['tope'].latitud,
                'longitud': pila_data['tope'].longitud,
            } if pila_data['tope'] else None,
            'elementos': [
                {
                    'id': str(elem.id),
                    'codigo': elem.codigo,
                    'direccion': elem.direccion,
                    'colonia': elem.colonia,
                    'posicion_pila': elem.posicion_pila,
                    'fecha_reporte': elem.fecha_reporte.strftime('%d/%m %H:%M'),
                }
                for elem in pila_data['elementos']
            ]
        }

    return JsonResponse({
        'status': 'ok',
        'pila_alto': serialize_pila(resumen['pila_alto']),
        'pila_medio': serialize_pila(resumen['pila_medio']),
        'pila_bajo': serialize_pila(resumen['pila_bajo']),
        'metricas': resumen['metricas'],
    })


# ==============================================================================
# AUTENTICACIÓN Y CONMUTADOR RÁPIDO DE ROLES
# ==============================================================================

def login_view(request):
    """
    Pantalla de autenticación con selector instantáneo de roles (Admin, Colaborador, Ciudadano)
    para evaluación rápida sin fricción.
    """
    if request.user.is_authenticated:
        return redirect('index')

    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            rol = get_user_role(user)
            messages.success(request, f"¡Bienvenido! Sesión iniciada como '{rol.upper()}'.")
            return redirect('index')
        else:
            error_msg = "Credenciales incorrectas. Verifica el usuario y la contraseña."

    return render(request, 'miapp/login.html', {'error_msg': error_msg})


def logout_view(request):
    """Cierra la sesión y redirige al login."""
    logout(request)
    messages.info(request, "Has cerrado tu sesión en el Sistema de Bacheo.")
    return redirect('login')


@login_required(login_url='login')
def cambiar_rol_demo(request, nuevo_rol):
    """
    Conmutador rápido de roles para facilitar la demostración y evaluación del sistema
    entre los tres perfiles: 'admin', 'colaborador' y 'ciudadano'.
    """
    nuevo_rol = nuevo_rol.lower()
    if nuevo_rol not in ['admin', 'colaborador', 'ciudadano']:
        messages.error(request, "Rol no reconocido.")
        return redirect('index')

    # Buscar el usuario de prueba correspondiente
    target_user = User.objects.filter(username=nuevo_rol).first()
    if target_user:
        login(request, target_user)
        messages.success(request, f"Cambio de rol exitoso: Ahora estás navegando como '{nuevo_rol.upper()}'.")
    else:
        # Si no existe, actualizar el rol del usuario actual
        perfil = get_perfil_usuario(request.user)
        if perfil:
            perfil.rol = nuevo_rol
            perfil.save()
            messages.success(request, f"Rol actualizado a '{nuevo_rol.upper()}'.")

    return redirect('index')


# ==============================================================================
# VISTAS DE SOPORTE COMPATIBLE (POS Y ANTERIORES)
# ==============================================================================

def modulo_cajero(request):
    """Vista de respaldo."""
    return redirect('index')


def procesar_venta_cajero(request):
    """Vista de respaldo."""
    return JsonResponse({'status': 'ok'})
