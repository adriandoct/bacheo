from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal adaptable al rol (Admin, Colaborador, Ciudadano)
    path('', views.index, name='index'),

    # Autenticación y Conmutador de Roles
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cambiar-rol-demo/<str:nuevo_rol>/', views.cambiar_rol_demo, name='cambiar_rol_demo'),

    # Operaciones fundamentales de la Pila (Stack LIFO)
    path('baches/registrar-push/', views.registrar_bache_push_view, name='registrar_bache_push'),
    path('baches/liberar-pop/', views.liberar_bache_pop_view, name='liberar_bache_pop'),
    path('baches/inspeccionar-peek/<str:nivel_riesgo>/', views.inspeccionar_peek_view, name='inspeccionar_peek'),

    # Reportes y Auditoría de Secuencia
    path('reportes/secuencia/', views.reportes_secuencia_view, name='reportes_secuencia'),
    path('reportes/exportar-csv/', views.exportar_reporte_csv, name='exportar_reporte_csv'),

    # API JSON para Google Maps y marcadores dinámicos
    path('api/baches/', views.api_baches_puntos, name='api_baches_puntos'),
    path('api/pilas-estado/', views.api_pilas_estado, name='api_pilas_estado'),

    # Vistas de soporte previas
    path('caja/', views.modulo_cajero, name='modulo_cajero'),
    path('caja/procesar-venta/', views.procesar_venta_cajero, name='procesar_venta_cajero'),
]
