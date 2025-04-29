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
def obtener_empleados(search_term='',termino_son_letras='',id_usuario=None,ip_usuario=None):
    
    connection.ensure_connection()
    conn = connection.connection
    
    if search_term:

        empleados = conn.execute("""
                EXEC sp_BuscarEmpleado 
                @searchTerm =?,
                @terminoSonLetras = ?,
                @idUsuario = ?,
                @ipUsuario = ?;
                """,(search_term, termino_son_letras, int(id_usuario), str(ip_usuario))).fetchall()
    else:
        query = "EXEC sp_obtenerEmpleados @idUsuario = ?"
        empleados = conn.execute(query, id_usuario).fetchall()

    # Se convierten los resultados a una lista de diccionarios
    empleados_list = [{'nombre': row[0],'identificacion': row[1],} for row in empleados]
    return empleados_list if empleados else []
    
#-------------------------------------------------------------
# Función para manejar la búsqueda de empleados desde AJAX
def buscar_empleados(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            id_usuario = request.session.get("_auth_user_id")
            ip_usuario = request.session.get("_auth_user_ip")
            termino_por_buscar = request.GET.get("term", '')
            termino_son_letras = request.GET.get("terminoSonLetras", '')
            empleados = obtener_empleados(termino_por_buscar,termino_son_letras,id_usuario,ip_usuario)
            
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

        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")
        

        try:
            #Aseguarar conexion
            connection.ensure_connection()
            conn = connection.connection

            # 5) Llamada al SP con los 5 parámetros
            conn.execute(
                "EXEC dbo.sp_AgregarEmpleado ?, ?, ?, ?, ?",
                [valor_doc, nombre, puesto, id_usuario, ip_usuario]
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
    if request.method == "POST" and request.headers.get("X-Requested-With"):

        # Obtener los datos del formulario
        old_doc       = request.POST.get("ident_old", "").strip()
        new_doc       = request.POST.get("ident_new", "").strip()
        nombre        = request.POST.get("nombre", "").strip()
        nombre_puesto = request.POST.get("puesto", "").strip()
        id_usuario    = request.session.get("_auth_user_id")
        ip_usuario    = request.session.get("_auth_user_ip")

        try:
            # Asegurar conexión
            connection.ensure_connection()
            conn = connection.connection
            # Ejecutar el procedimiento almacenado para actualizar el empleado
            conn.execute(
                """
                EXEC dbo.sp_ActualizarEmpleado
                    @ValorDocumentoIdentidadOld = ?,
                    @ValorDocumentoIdentidadNew = ?,
                    @Nombre                     = ?,
                    @NombrePuesto               = ?,
                    @UsuarioId                  = ?,
                    @IpUsuario                  = ?
                """,
                [old_doc, new_doc, nombre, nombre_puesto, id_usuario, ip_usuario]
            )
            return JsonResponse({
                "success": True,
                "mensaje": "Empleado actualizado correctamente"
            })
        except Exception as e:
            # Capturar cualquier error que lance el THROW del SP
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "success": False,
        "error": "Método no permitido"
    }, status=400)

#-------------------------------------------------------------
# Función para eliminar un empleado
def delete_empleado(request):
    if request.method == "POST" and request.headers.get("X-Requested-With"):
        valor_doc   = request.POST.get("identificacion", "").strip()
        confirmar   = request.POST.get("confirmar", "1")  # "1"=confirmar, "0"=cancelar
        id_usuario  = request.session.get("_auth_user_id")
        ip_usuario  = request.session.get("_auth_user_ip")

        try:
            connection.ensure_connection()
            conn = connection.connection
            conn.execute(
                """
                EXEC dbo.sp_EliminarEmpleado
                    @ValorDocumentoIdentidad = ?,
                    @UsuarioId               = ?,
                    @IpUsuario               = ?,
                    @Confirmar               = ?
                """,
                [valor_doc, id_usuario, ip_usuario, int(confirmar)]
            )
            # Mensaje distinto según confirmación o intento
            mensaje = (
                "Empleado eliminado correctamente"
                if confirmar == "1"
                else "Intento de borrado registrado en bitácora"
            )
            return JsonResponse({"success": True, "mensaje": mensaje})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

#-------------------------------------------------------------
#Funcion para consultar un empleado
def consultar_empleado(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        valor      = request.GET.get('identificacion', '').strip()
        id_usuario = request.session.get("_auth_user_id") or 0

        try:
            connection.ensure_connection()
            conn = connection.connection
            row = conn.execute(
                "EXEC dbo.sp_ConsultarEmpleado @ValorDocumentoIdentidad = ?, @UsuarioId = ?",
                [valor, int(id_usuario)]
            ).fetchone()

            if not row:
                return JsonResponse({"success": False, "error": "Empleado no encontrado"}, status=404)

            empleado = {
                "identificacion": row[0],
                "nombre":         row[1],
                "puesto":         row[2],
                "saldoVacaciones": float(row[3]),
            }
            return JsonResponse({"success": True, "empleado": empleado})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

#-------------------------------------------------------------
#funcion para obtener el saldo de vacaciones de un empleado
def obtener_saldo_vacaciones(request):
    pass

def movimientos(request, identificacion):
    
    try:
        id_usuario = request.session.get("_auth_user_id")
        nombre  = request.GET.get("nombre", "").strip()
        
        connection.ensure_connection()
        conn = connection.connection

        saldo = conn.execute(
            """
            EXEC dbo.sp_GetSaldo
                @idUsuario = ?,
                @identificacion = ?
            """,
            (int(id_usuario), identificacion)).fetchone()[0]
            
            
        movimientos = conn.execute(
                """
                EXEC dbo.sp_ObtenerMovimientos 
                    @idUsuario = ?,
                    @ValorDocumentoIdentidad = ?
                """,
                (int(id_usuario), identificacion)).fetchall()

        # Convertir los resultados a una lista de diccionarios
        movimientos_list = [{
            'fecha': row[0],
            'tipo': row[1],
            'monto': float(row[2]) if row[2] else 0.0, 
            'saldo': float(row[3]) if row[3] else 0.0,
            'usuario': row[4], 
            'ip': row[5], 
            'hora': row[6]
            } for row in movimientos]
        return render(request, "movimientos.html", {
                "movimientos": movimientos_list,
                "identificacion": identificacion,
                "nombre": nombre,
                "saldo": saldo,
                "error": None
                })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def insertar_movimiento(request):
    #if request.headers.get("X-Requested-With") == "XMLHttpRequest":
    if request.method == "POST":
        try:
            print("Insertando movimiento---------------------------")
            id_usuario = request.session.get("_auth_user_id")
            ip_usuario = request.session.get("_auth_user_ip")
            identificacion = request.POST.get("identificacion", "").strip()
            tipo = request.POST.get("tipo_movimiento", "").strip()
            monto = float(request.POST.get("monto", 0.0))

            connection.ensure_connection()
            conn = connection.connection

            print(f"Datos recibidos: id={identificacion}, tipo={tipo}, monto={monto}")  # Debug log
            conn.execute(
                """
                EXEC dbo.sp_AgregarMovimiento 
                    @idUsuario = ?,
                    @ipUsuario = ?,
                    @identificacion = ?,
                    @idTipoMovimiento = ?,
                    @monto = ?
                """,
                (int(id_usuario), str(ip_usuario), identificacion.strip(), tipo.strip(), float(monto))
            )
            return JsonResponse({"success": True, "mensaje": "Movimiento agregado correctamente"})
        except Exception as e:
            print(f"Error al insertar movimiento: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)