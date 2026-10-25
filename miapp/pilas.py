"""
Módulo de Estructura de Datos: Pilas (Stack - LIFO: Last-In, First-Out)
========================================================================
Implementación rigurosa de estructuras de control y tipos abstractos de datos (TAD)
para la gestión secuencial de bacheo en Tijuana, B.C., almacenado en MongoDB.

Autor: Senior Software Engineer
"""

from typing import Any, List, Optional, Tuple, Dict
from django.utils import timezone
from .models import Bache, SecuenciaOperacionPila, Usuario


class PilaVaciaException(Exception):
    """Excepción lanzada cuando se intenta una operación POP o PEEK sobre una pila sin elementos."""
    pass


class BacheInvalidoException(Exception):
    """Excepción lanzada cuando los datos de un bache no cumplen con las validaciones de negocio."""
    pass


class NodoPila:
    """
    Nodo individual de una lista enlazada simple para la implementación de la Pila.
    Complejidad espacial: O(1) por nodo.
    """
    def __init__(self, valor: Any, siguiente: Optional['NodoPila'] = None):
        self.valor = valor
        self.siguiente = siguiente

    def __repr__(self) -> str:
        return f"NodoPila(valor={self.valor})"


class Pila:
    """
    Estructura de datos lineal tipo Pila (LIFO: Last-In, First-Out).
    Todas las operaciones principales (push, pop, peek, is_empty) operan en tiempo constante O(1).
    """

    def __init__(self, nombre: str = "Pila General"):
        self.nombre: str = nombre
        self._tope: Optional[NodoPila] = None
        self._tamano: int = 0

    def is_empty(self) -> bool:
        """Determina si la pila carece de elementos. Complejidad: O(1)."""
        return self._tope is None

    def size(self) -> int:
        """Retorna el número actual de elementos contenidos en la pila. Complejidad: O(1)."""
        return self._tamano

    def push(self, elemento: Any) -> None:
        """
        Inserta un nuevo elemento en la cima (tope) de la pila.
        Complejidad: O(1).
        """
        nuevo_nodo = NodoPila(valor=elemento, siguiente=self._tope)
        self._tope = nuevo_nodo
        self._tamano += 1

    def pop(self) -> Any:
        """
        Extrae y remueve el elemento situado en el tope de la pila.
        Lanza PilaVaciaException si la pila se encuentra vacía.
        Complejidad: O(1).
        """
        if self.is_empty():
            raise PilaVaciaException(f"La pila '{self.nombre}' no contiene baches pendientes para liberar.")
        
        nodo_extraido = self._tope
        self._tope = self._tope.siguiente
        self._tamano -= 1
        return nodo_extraido.valor

    def peek(self) -> Any:
        """
        Inspecciona el elemento ubicado en el tope sin removerlo de la estructura.
        Complejidad: O(1).
        """
        if self.is_empty():
            return None
        return self._tope.valor

    def to_list(self) -> List[Any]:
        """
        Retorna la representación secuencial de los elementos desde el TOPE hasta la BASE.
        Complejidad: O(n).
        """
        elementos = []
        actual = self._tope
        while actual is not None:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def clear(self) -> None:
        """Vacía completamente la pila."""
        self._tope = None
        self._tamano = 0

    def __len__(self) -> int:
        return self._tamano

    def __repr__(self) -> str:
        return f"<Pila '{self.nombre}': {self._tamano} elementos, Tope={self.peek()}>"


class GestorPilasBacheo:
    """
    Controlador y orquestador empresarial de pilas para bacheo en Tijuana.
    Mantiene 3 pilas especializadas por nivel de criticidad (Alto, Mediano, Bajo Riesgo)
    y sincroniza su estado con los documentos de MongoDB, generando auditoría de secuencias.
    """

    NOMBRES_PILAS = {
        'alto': 'Pila de Alto Riesgo (Emergencia Vial)',
        'medio': 'Pila de Mediano Riesgo (Afectación Regular)',
        'bajo': 'Pila de Bajo Riesgo (Mantenimiento Preventivo)',
    }

    @classmethod
    def generar_codigo_bache(cls) -> str:
        """Genera un código secuencial profesional único con nomenclatura oficial."""
        ahora = timezone.now()
        anio = ahora.year
        total_hoy = Bache.objects.filter(fecha_reporte__year=anio).count() + 1
        return f"BACH-TJ-{anio}-{total_hoy:04d}"

    @classmethod
    def cargar_pila_desde_bd(cls, nivel_riesgo: str) -> Pila:
        """
        Reconstruye la pila en memoria desde la base de datos MongoDB.
        Los baches pendientes se ordenan de BASE a TOPE para que al aplicar PUSH
        el último registrado quede exactamente en la cima (LIFO).
        """
        nombre = cls.NOMBRES_PILAS.get(nivel_riesgo, f"Pila {nivel_riesgo}")
        pila = Pila(nombre=nombre)

        # Obtenemos los pendientes del más antiguo al más reciente (base -> tope)
        baches = Bache.objects.filter(
            nivel_riesgo=nivel_riesgo,
            estado='pendiente'
        ).order_by('fecha_reporte')

        for bache in baches:
            pila.push(bache)

        return pila

    @classmethod
    def registrar_bache_push(
        cls,
        datos: Dict[str, Any],
        usuario_operador: Optional[Usuario] = None
    ) -> Tuple[Bache, SecuenciaOperacionPila]:
        """
        Operación PUSH:
        1. Valida las estructuras de datos y parámetros geográficos en Tijuana.
        2. Determina el nivel de riesgo (alto, medio, bajo).
        3. Persiste el documento en MongoDB en la colección 'baches'.
        4. Registra la transición en la colección 'secuencias_pila' (evento PUSH).
        """
        nivel = datos.get('nivel_riesgo', 'medio').lower()
        if nivel not in ['alto', 'medio', 'bajo']:
            nivel = 'medio'

        direccion = datos.get('direccion', '').strip()
        if not direccion:
            raise BacheInvalidoException("La dirección en Tijuana es obligatoria para geolocalizar el bache.")

        # Cargar pila actual para conocer el estado y tope previo
        pila_actual = cls.cargar_pila_desde_bd(nivel)
        tamano_antes = pila_actual.size()
        tope_previo = pila_actual.peek()
        tope_previo_codigo = tope_previo.codigo if tope_previo else "PILA_VACIA"

        # Construir código único
        codigo = cls.generar_codigo_bache()

        # Posición calculada para el nuevo elemento en el tope
        nueva_posicion = tamano_antes + 1

        # Crear y persistir el bache en MongoDB
        nuevo_bache = Bache.objects.create(
            codigo=codigo,
            ciudadano=usuario_operador if (usuario_operador and usuario_operador.es_ciudadano) else None,
            nivel_riesgo=nivel,
            estado='pendiente',
            direccion=direccion,
            colonia=datos.get('colonia', 'Zona Urbana Río').strip(),
            ciudad="Tijuana",
            codigo_postal=datos.get('codigo_postal', '22000').strip(),
            latitud=float(datos.get('latitud', 32.5149469)),
            longitud=float(datos.get('longitud', -117.0382471)),
            referencias=datos.get('referencias', '').strip(),
            descripcion=datos.get('descripcion', '').strip(),
            diametro_estimado=datos.get('diametro_estimado', '60 cm').strip(),
            profundidad_estimada=datos.get('profundidad_estimada', '12 cm').strip(),
            foto_url=datos.get('foto_url', '').strip(),
            pila_tipo=nivel,
            posicion_pila=nueva_posicion,
        )

        # Actualizar estructura en memoria
        pila_actual.push(nuevo_bache)
        tamano_despues = pila_actual.size()
        tope_nuevo_codigo = nuevo_bache.codigo

        # Registrar la secuencia de auditoría
        rol_nombre = usuario_operador.rol if usuario_operador else "anónimo"
        secuencia = SecuenciaOperacionPila.objects.create(
            bache=nuevo_bache,
            tipo_operacion='PUSH',
            pila_nombre=cls.NOMBRES_PILAS.get(nivel, nivel),
            usuario=usuario_operador,
            rol_usuario=rol_nombre,
            posicion_en_pila=nueva_posicion,
            tamano_pila_antes=tamano_antes,
            tamano_pila_despues=tamano_despues,
            tope_codigo_previo=tope_previo_codigo,
            tope_codigo_nuevo=tope_nuevo_codigo,
            descripcion=(
                f"OPERACIÓN PUSH: Registro exitoso del bache {codigo} [{nivel.upper()} RIESGO] "
                f"en la cima de la pila. Posición: {nueva_posicion}. Ubicación: {nuevo_bache.direccion}, {nuevo_bache.colonia}."
            )
        )

        return nuevo_bache, secuencia

    @classmethod
    def liberar_bache_pop(
        cls,
        nivel_riesgo: str,
        colaborador_usuario: Optional[Usuario] = None,
        notas_reparacion: str = "",
        material_utilizado: str = "Mezcla Asfáltica en Caliente",
        bache_especifico_id: Optional[str] = None
    ) -> Tuple[Bache, SecuenciaOperacionPila]:
        """
        Operación POP:
        1. Localiza el bache situado en el TOPE de la pila de riesgo especificada.
        2. Si se proporciona un id específico (o por defecto el tope LIFO), se atiende y libera.
        3. Actualiza el estado a 'atendido', marca de tiempo de liberación y notas.
        4. Registra el evento POP en 'secuencias_pila' con las métricas del proceso.
        """
        nivel = nivel_riesgo.lower()
        pila_actual = cls.cargar_pila_desde_bd(nivel)

        if pila_actual.is_empty():
            raise PilaVaciaException(
                f"No existen baches pendientes en la {cls.NOMBRES_PILAS.get(nivel, nivel)}. La pila está vacía."
            )

        tamano_antes = pila_actual.size()
        bache_a_liberar: Optional[Bache] = None

        if bache_especifico_id:
            try:
                bache_a_liberar = Bache.objects.get(id=bache_especifico_id, estado='pendiente')
            except Bache.DoesNotExist:
                bache_a_liberar = pila_actual.peek()
        else:
            # Por definición de Pila LIFO, se atiende el último bache ingresado (TOPE)
            bache_a_liberar = pila_actual.peek()

        if not bache_a_liberar:
            raise PilaVaciaException("No se encontró ningún bache elegible para ser liberado en esta pila.")

        # Calcular tiempo de atención en minutos
        ahora = timezone.now()
        tiempo_delta = ahora - bache_a_liberar.fecha_reporte
        minutos = max(1, int(tiempo_delta.total_seconds() // 60))

        # Modificar estado en MongoDB
        bache_a_liberar.estado = 'atendido'
        bache_a_liberar.fecha_liberacion = ahora
        bache_a_liberar.atendido_por = colaborador_usuario
        bache_a_liberar.notas_reparacion = notas_reparacion or "Bache atendido y sellado conforme a norma técnica de obras públicas."
        bache_a_liberar.material_utilizado = material_utilizado or "Mezcla Asfáltica en Caliente y Polímero"
        bache_a_liberar.tiempo_atencion_minutos = minutos
        bache_a_liberar.save()

        # Recargar pila para calcular nuevo tope
        pila_posterior = cls.cargar_pila_desde_bd(nivel)
        tamano_despues = pila_posterior.size()
        nuevo_tope = pila_posterior.peek()
        nuevo_tope_codigo = nuevo_tope.codigo if nuevo_tope else "PILA_VACIA"

        # Registrar evento POP en la secuencia de auditoría
        rol_nombre = colaborador_usuario.rol if colaborador_usuario else "colaborador"
        secuencia = SecuenciaOperacionPila.objects.create(
            bache=bache_a_liberar,
            tipo_operacion='POP',
            pila_nombre=cls.NOMBRES_PILAS.get(nivel, nivel),
            usuario=colaborador_usuario,
            rol_usuario=rol_nombre,
            posicion_en_pila=1,
            tamano_pila_antes=tamano_antes,
            tamano_pila_despues=tamano_despues,
            tope_codigo_previo=bache_a_liberar.codigo,
            tope_codigo_nuevo=nuevo_tope_codigo,
            descripcion=(
                f"OPERACIÓN POP: Bache {bache_a_liberar.codigo} reparado y liberado exitosamente "
                f"por el colaborador '{colaborador_usuario.nombre_completo if colaborador_usuario else 'Cuadrilla Municipal'}'. "
                f"Tiempo de respuesta: {minutos} min. Nuevo tope: {nuevo_tope_codigo}."
            )
        )

        return bache_a_liberar, secuencia

    @classmethod
    def obtener_resumen_pilas(cls) -> Dict[str, Any]:
        """
        Retorna un panorama integral de las pilas y métricas del sistema
        para los paneles de control de Admin, Colaborador y Ciudadano.
        """
        pila_alto = cls.cargar_pila_desde_bd('alto')
        pila_medio = cls.cargar_pila_desde_bd('medio')
        pila_bajo = cls.cargar_pila_desde_bd('bajo')

        total_pendientes = pila_alto.size() + pila_medio.size() + pila_bajo.size()
        total_atendidos = Bache.objects.filter(estado='atendido').count()
        total_registros = Bache.objects.count()

        # Secuencias recientes
        ultimas_secuencias = SecuenciaOperacionPila.objects.select_related('bache', 'usuario').all()[:15]

        return {
            'pila_alto': {
                'objeto': pila_alto,
                'tamano': pila_alto.size(),
                'tope': pila_alto.peek(),
                'elementos': pila_alto.to_list(),
                'nombre': cls.NOMBRES_PILAS['alto'],
                'color': 'danger',
            },
            'pila_medio': {
                'objeto': pila_medio,
                'tamano': pila_medio.size(),
                'tope': pila_medio.peek(),
                'elementos': pila_medio.to_list(),
                'nombre': cls.NOMBRES_PILAS['medio'],
                'color': 'warning',
            },
            'pila_bajo': {
                'objeto': pila_bajo,
                'tamano': pila_bajo.size(),
                'tope': pila_bajo.peek(),
                'elementos': pila_bajo.to_list(),
                'nombre': cls.NOMBRES_PILAS['bajo'],
                'color': 'info',
            },
            'metricas': {
                'total_pendientes': total_pendientes,
                'total_atendidos': total_atendidos,
                'total_registros': total_registros,
                'tasa_efectividad': round((total_atendidos / total_registros * 100), 1) if total_registros > 0 else 0,
            },
            'ultimas_secuencias': ultimas_secuencias,
        }
