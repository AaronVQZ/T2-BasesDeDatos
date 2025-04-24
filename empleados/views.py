from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
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

    #return render(request, "home.html", {"empleados": lista_empleados})


def obtener_empleados(search_term=''):
    
    connection.ensure_connection()
    conn = connection.connection
    
    if search_term:
        query = "EXEC sp_BuscarEmpleado ?"
        empleados = conn.execute(query,[search_term]).fetchall()
    else:
        query = "EXEC sp_obtenerEmpleados"
        empleados = conn.execute(query).fetchall()
        print(empleados)

    empleados_list = [{'nombre': row[0],'identificacion': row[1],} for row in empleados]
    print(f'\n\nlista 2 {empleados_list}')


    return empleados_list if empleados else []
    

    
def buscar_empleados(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            search_term = request.GET.get("term", '')
            empleados = obtener_empleados(search_term)
            print(empleados)
            return JsonResponse({"success": True, "empleados": empleados}, safe=False)
        except Exception as e:
            return JsonResponse({"success": True, "error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

