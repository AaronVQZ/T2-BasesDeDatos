from django.urls import path
from . import views

app_name = "empleados"

urlpatterns = [
    path("", views.home, name="home"),
    path("buscar-empleados/", views.buscar_empleados, name="buscar_empleados"),
    path("insertar-empleado/", views.insertar_empleado, name="insertar_empleado"),  
    path("consultar-empleado/", views.consultar_empleado, name="consultar_empleado"),
    path("borrar-empleado/", views.delete_empleado, name="borrar_empleado"),
    path("update-empleado/", views.update_empleado, name="update_empleado"),
]
