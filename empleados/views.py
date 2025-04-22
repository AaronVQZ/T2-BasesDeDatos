from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
def home(request):

    lista_empleados = obtener_empleados()

    return render(request, "home.html", {"empleados": lista_empleados})


def obtener_empleados():
    
    query = "EXEC sp_obtenerEmpleados"
    connection.ensure_connection()
    conn = connection.connection
    empleados = conn.execute(query).fetchall()
    return empleados
    

