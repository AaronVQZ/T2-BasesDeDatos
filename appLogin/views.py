from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json


#Vista de inicio de sesión

def login(request):
    #Verificar si la solicitud es POST. Envio de formulario o JSON
    if request.method == "POST":
        ip = request.META.get('REMOTE_ADDR') # Obtener la IP del cliente

        # Verificar si los datos vienen en formato JSON
        if request.content_type == "application/json":

            try:
                #Cargar datos desde el cuerpo de la solicitud
                data = json.loads(request.body) 

            except json.JSONDecodeError:
                # Manejar error de JSON inválido
                return JsonResponse({"error": "Datos inválidos"}, status=400)
            
            # Obtener los datos del JSON
            username = data.get('username', '')
            password = data.get('password', '')

        else:
            # Si no es JSON, obtener los datos del formulario
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')


        # Imprimir los datos recibidos (Verificacion)
        print(f"Datos recibidos: username={username}, password={password}")

        try:
            # Verificar si la conexión está activa
            connection.ensure_connection()
            conn = connection.connection

            # Ejecutar SP para verificar si la IP está bloqueada
            result = conn.execute("""
                DECLARE @IntentosRecientes INT, @EstaBloqueado BIT;
                EXEC dbo.sp_VerificarIntentosFallidos 
                    @IP = ?, 
                    @IntentosRecientes = @IntentosRecientes OUTPUT,
                    @EstaBloqueado = @EstaBloqueado OUTPUT;
                SELECT @IntentosRecientes AS IntentosRecientes, @EstaBloqueado AS EstaBloqueado;
            """, (ip,)).fetchone()

            #En caso de que la IP esté bloqueada, se retorna un mensaje de error
            if result and result[1]:  # @EstaBloqueado
                return JsonResponse({
                    "error": "blocked",
                    "message": "Demasiados intentos. Espere 10 minutos."
                }, status=403)

            # Si no está bloqueada, se procede a verificar las credenciales, por medio del SP
            result = conn.execute("""
                DECLARE @EsValido BIT, @Mensaje VARCHAR(200);
                EXEC dbo.sp_ValidarUsuario 
                    @Username = ?, 
                    @Password = ?, 
                    @IP = ?, 
                    @EsValido = @EsValido OUTPUT, 
                    @Mensaje = @Mensaje OUTPUT;
                SELECT @EsValido AS EsValido, @Mensaje AS Mensaje;
            """, (username, password, ip)).fetchone()

            #Obtenrer el resultado de la validación
            es_valido, mensaje = result

            # Mostrar si las credenciales son válidas (Verificacion)
            print(f"Es válido: {es_valido}, Mensaje: {mensaje}")

            # Si las credenciales son válidas, se redirige al usuario a la página de inicio
            if es_valido:
                return JsonResponse({"success": True, "redirect": "/home"})
            else:
                # Si las credenciales no son válidas, se retorna un mensaje de error
                return JsonResponse({"error": "invalid_credentials", "message": mensaje}, status=400)

        except Exception as e:
            # Si ocurre un error al ejecutar el SP, se maneja la excepción y se retorna un mensaje de error
            print(f"Error de base de datos: {str(e)}")
            return JsonResponse({"error": "database_error", "message": str(e)}, status=500)

    # En caso de que sea una solicitud GET, se verifica si la IP está bloqueada al cargar la pagina para bloquear el boton de inicio de sesión
    if request.method == "GET":
        ip = request.META.get('REMOTE_ADDR')
        try:
            connection.ensure_connection()
            conn = connection.connection

            #Verificar si la IP está bloqueada al cargar la página
            result = conn.execute("""
                DECLARE @IntentosRecientes INT, @EstaBloqueado BIT;
                EXEC dbo.sp_VerificarIntentosFallidos 
                    @IP = ?, 
                    @IntentosRecientes = @IntentosRecientes OUTPUT,
                    @EstaBloqueado = @EstaBloqueado OUTPUT;
                SELECT @IntentosRecientes AS IntentosRecientes, @EstaBloqueado AS EstaBloqueado;
            """, (ip,)).fetchone()

            #En caso de que la IP esté bloqueada, se muestrra un aviso
            if result and result[1]:
                return render(request, "login.html", {"blocked": True})

        except Exception:
            pass  # Ignorar y continuar

    return render(request, "login.html", {"blocked": False})

