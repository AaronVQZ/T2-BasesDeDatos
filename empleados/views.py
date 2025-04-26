import traceback
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
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
    if request.method == "POST" and request.headers.get("X-Requested-With"):
        #Obtenr los datos del formulario
        valor_doc = request.POST.get("identificacion", "").strip()
        nombre    = request.POST.get("nombre", "").strip()
        puesto    = request.POST.get("puesto", "").strip()

        #Definir el id del usuario
        id_user   = 7

        #Obtener la IP del cliente
        ip_cliente = request.META.get("REMOTE_ADDR", "")

        try:
            #Aseguarar conexion
            connection.ensure_connection()
            conn = connection.connection

            # 5) Llamada al SP con los 5 parámetros
            conn.execute(
                "EXEC dbo.sp_AgregarEmpleado ?, ?, ?, ?, ?",
                [valor_doc, nombre, puesto, id_user, ip_cliente]
            )

            # Si no hay excepción, devolvemos JSON de éxito
            return JsonResponse({"success": True, "mensaje": "Empleado insertado correctamente"})

        except Exception as e:
            # Capturar cualquier error que lance el THROW del SP
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # Si no es POST AJAX
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)
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
