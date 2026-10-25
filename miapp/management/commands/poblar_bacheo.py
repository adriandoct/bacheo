"""
Comando de inicialización y siembra de datos para el Sistema Inteligente de Bacheo Tijuana.
Crea usuarios predeterminados (Admin, Colaborador, Ciudadano) y genera baches iniciales
organizados en sus respectivas pilas de riesgo con coordenadas reales de Tijuana.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from miapp.models import Usuario, Bache, SecuenciaOperacionPila
from miapp.pilas import GestorPilasBacheo


class Command(BaseCommand):
    help = "Siembra usuarios de prueba (Admin, Colaborador, Ciudadano) y baches en Tijuana"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando siembra de datos para el Sistema de Bacheo Tijuana..."))

        # 1. Crear o actualizar usuarios con roles definidos
        usuarios_datos = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@tijuana.gob.mx',
                'nombre': 'Ing. Roberto Santana (Admin Obras Públicas)',
                'telefono': '664-123-4567',
                'rol': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'colaborador',
                'password': 'colaborador123',
                'email': 'cuadrilla.centro@tijuana.gob.mx',
                'nombre': 'Téc. Marco Domínguez (Brigada Rápida Otay-Río)',
                'telefono': '664-987-6543',
                'rol': 'colaborador',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'ciudadano',
                'password': 'ciudadano123',
                'email': 'ciudadano.tijuana@gmail.com',
                'nombre': 'Valeria Méndez (Vecina de Playas de Tijuana)',
                'telefono': '664-555-8899',
                'rol': 'ciudadano',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        usuarios_creados = {}
        for u_data in usuarios_datos:
            auth_user, created = User.objects.get_or_create(username=u_data['username'])
            auth_user.email = u_data['email']
            auth_user.is_staff = u_data['is_staff']
            auth_user.is_superuser = u_data['is_superuser']
            auth_user.set_password(u_data['password'])
            auth_user.save()

            perfil, p_created = Usuario.objects.get_or_create(user=auth_user)
            perfil.username = u_data['username']
            perfil.email = u_data['email']
            perfil.nombre_completo = u_data['nombre']
            perfil.telefono = u_data['telefono']
            perfil.rol = u_data['rol']
            perfil.save()
            usuarios_creados[u_data['username']] = perfil

            estado_txt = "creado" if created else "actualizado"
            self.stdout.write(self.style.SUCCESS(f"Usuario '{u_data['username']}' [{u_data['rol']}] {estado_txt}."))

        # 2. Baches iniciales en puntos clave de Tijuana
        baches_semilla = [
            # Alto riesgo
            {
                'direccion': 'Paseo de los Héroes 9500, frente a Plaza Río',
                'colonia': 'Zona Urbana Río',
                'codigo_postal': '22010',
                'latitud': 32.527351,
                'longitud': -117.020582,
                'nivel_riesgo': 'alto',
                'descripcion': 'Bache profundo de 20cm en carril de alta velocidad, expone varilla y genera daño a rines.',
                'diametro_estimado': '95 cm',
                'profundidad_estimada': '22 cm',
                'referencias': 'Entre calle Diego Rivera y Blvd. Cuauhtémoc Norte',
            },
            {
                'direccion': 'Vía Rápida Poniente km 4.5, carril izquierdo',
                'colonia': '20 de Noviembre',
                'codigo_postal': '22100',
                'latitud': 32.508492,
                'longitud': -116.989211,
                'nivel_riesgo': 'alto',
                'descripcion': 'Hundimiento en junta de puente sobre canalización, alto riesgo de volcadura en tráfico rápido.',
                'diametro_estimado': '120 cm',
                'profundidad_estimada': '18 cm',
                'referencias': 'Cerca del puente peatonal 20 de Noviembre',
            },
            # Mediano riesgo
            {
                'direccion': 'Blvd. Agua Caliente 10500, frente a Galerías Hipódromo',
                'colonia': 'Aviación',
                'codigo_postal': '22014',
                'latitud': 32.509823,
                'longitud': -117.001923,
                'nivel_riesgo': 'medio',
                'descripcion': 'Desgaste severo del asfalto por fuga de agua ya reparada. Provoca frenado brusco.',
                'diametro_estimado': '65 cm',
                'profundidad_estimada': '12 cm',
                'referencias': 'Frente al acceso al estacionamiento subterráneo',
            },
            {
                'direccion': 'Av. de las Ferias 430, casi esq. con Paseo del Prado',
                'colonia': 'Lomas Hipódromo',
                'codigo_postal': '22030',
                'latitud': 32.496512,
                'longitud': -116.994812,
                'nivel_riesgo': 'medio',
                'descripcion': 'Bache en carril derecho frente a parada de transporte público.',
                'diametro_estimado': '50 cm',
                'profundidad_estimada': '10 cm',
                'referencias': 'A 50 metros del OXXO Las Ferias',
            },
            # Bajo riesgo
            {
                'direccion': 'Paseo Pedregal 1250, esquina con Parque México Sur',
                'colonia': 'Playas de Tijuana',
                'codigo_postal': '22500',
                'latitud': 32.531201,
                'longitud': -117.121543,
                'nivel_riesgo': 'bajo',
                'descripcion': 'Agrietamiento superficial y desprendimiento de gravilla en calle residencial tranquila.',
                'diametro_estimado': '40 cm',
                'profundidad_estimada': '5 cm',
                'referencias': 'Frente al parque infantil de Playas',
            },
            {
                'direccion': 'Blvd. Bellas Artes 19800, cruce con Av. Vidal y Planas',
                'colonia': 'Ciudad Industrial Otay',
                'codigo_postal': '22444',
                'latitud': 32.539811,
                'longitud': -116.945231,
                'nivel_riesgo': 'bajo',
                'descripcion': 'Desnivel leve en orilla de acotamiento por tránsito de carga pesada.',
                'diametro_estimado': '45 cm',
                'profundidad_estimada': '6 cm',
                'referencias': 'Zona de naves industriales cerca de Garita de Otay',
            },
        ]

        ciudadano_user = usuarios_creados['ciudadano']
        colaborador_user = usuarios_creados['colaborador']

        # Si no hay baches creados previamente, registrar la semilla mediante PUSH en la Pila
        if Bache.objects.count() == 0:
            self.stdout.write(self.style.NOTICE("Insertando baches mediante operación PUSH en las Pilas de Tijuana..."))
            for b_data in baches_semilla:
                bache_obj, seq = GestorPilasBacheo.registrar_bache_push(
                    datos=b_data,
                    usuario_operador=ciudadano_user
                )
                self.stdout.write(self.style.SUCCESS(f"PUSH completado: {bache_obj.codigo} -> {b_data['colonia']}"))

            # Realizar un POP de demostración sobre uno de mediano riesgo para ilustrar la liberación
            try:
                bache_liberado, seq_pop = GestorPilasBacheo.liberar_bache_pop(
                    nivel_riesgo='medio',
                    colaborador_usuario=colaborador_user,
                    notas_reparacion="Se aplicó emulsión catiónica y 3 carretillas de asfalto caliente compactado con rodillo vibratorio.",
                    material_utilizado="Mezcla Asfáltica Templada AC-20 con Polímero"
                )
                self.stdout.write(self.style.SUCCESS(f"POP completado: {bache_liberado.codigo} ha sido ATENDIDO y LIBERADO."))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Aviso durante demo POP: {e}"))
        else:
            self.stdout.write(self.style.NOTICE("Ya existen baches en la base de datos 'bacheo'. No se duplicaron."))

        self.stdout.write(self.style.SUCCESS("[OK] Inicializacion de datos para Bacheo Tijuana completada con exito."))
