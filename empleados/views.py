from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

#-------------------------------------------------------------
# Vista principal que muestra la lista de empleados

def home(request):
    search_query = request.GET.get("search", '')

    try:
        lista_empleados = obtener_empleados(search_query)
        return render(request, "home.html", {
                "empleados": lista_empleados,
                "search_query": search_query
                })
    except Exception as e:
        return render(request, "home.html", {
            "error": "Error al obtener empleados",
            "search_query": search_query
        })

#-------------------------------------------------------------
# Función para obtener empleados desde la base de datos
def obtener_empleados(search_term=''):
    
    connection.ensure_connection()
    conn = connection.connection
    
    if search_term:
        query = "EXEC sp_BuscarEmpleado ?"
        empleados = conn.execute(query,[search_term]).fetchall()
    else:
        query = "EXEC sp_obtenerEmpleados"
        empleados = conn.execute(query).fetchall()

    # Se convierten los resultados a una lista de diccionarios
    empleados_list = [{'nombre': row[0],'identificacion': row[1],} for row in empleados]
    return empleados_list if empleados else []
    
#-------------------------------------------------------------
# Función para manejar la búsqueda de empleados desde AJAX
def buscar_empleados(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            termino_por_buscar = request.GET.get("term", '')
            empleados = obtener_empleados(termino_por_buscar)
            return JsonResponse({"success": True, "empleados": empleados}, safe=False)

        except Exception as e:
            return JsonResponse({"success": True, "error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

#-------------------------------------------------------------
# Función para insertar un nuevo empleado
def insertar_empleado(request):
    print("insertar_empleado")
#-------------------------------------------------------------
# Función para actualizar un empleado existente
def update_empleado(request):
    print("update_empleado")

#-------------------------------------------------------------
# Función para eliminar un empleado
def delete_empleado(request):
    print("delete_empleado")

#-------------------------------------------------------------
# Función para consultar un empleado específico
def consular_empleado(request):
    print("consultar_empleado")
