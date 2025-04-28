from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json

def login(request):
    if request.method == "POST":
        ip = request.META.get('REMOTE_ADDR')

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Datos inválidos"}, status=400)

            username = data.get('username', '')
            password = data.get('password', '')
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

        print(f"Datos recibidos: username={username}, password={password}")

        try:
            connection.ensure_connection()
            conn = connection.connection

            # Verificar si la IP está bloqueada
            result = conn.execute("""
                EXEC dbo.sp_VerificarIntentosFallidos @IP = ?
            """, (ip,)).fetchone()

            if result and result[1]:  # EstaBloqueado
                return JsonResponse({
                    "error": "blocked",
                    "message": "Demasiados intentos. Espere 10 minutos."
                }, status=403)

            # Validar usuario
            result = conn.execute("""
                EXEC dbo.sp_ValidarUsuario @Username = ?, @Password = ?, @IP = ?
            """, (username, password, ip)).fetchone()

            es_valido, mensaje = result

            print(f"Es válido: {es_valido}, Mensaje: {mensaje}")

            if es_valido:
                id_usuario = conn.execute("""
                    EXEC dbo.sp_GetIdUsuario @Username = ?, @Password = ?
                """, (username, password)).fetchone()[0]

                request.session['_auth_user_id'] = id_usuario
                request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
                request.session['_auth_user_ip'] = ip
                request.user = Usuario(id_usuario=id_usuario, username=username)

                return JsonResponse({"success": True, "redirect": "/home"})
            else:
                return JsonResponse({"error": "invalid_credentials", "message": mensaje}, status=400)

        except Exception as e:
            print(f"Error de base de datos: {str(e)}")
            return JsonResponse({"error": "database_error", "message": str(e)}, status=500)

    if request.method == "GET":
        ip = request.META.get('REMOTE_ADDR')
        try:
            connection.ensure_connection()
            conn = connection.connection

            result = conn.execute("""
                EXEC dbo.sp_VerificarIntentosFallidos @IP = ?
            """, (ip,)).fetchone()

            if result and result[1]:
                return render(request, "login.html", {"blocked": True})

        except Exception:
            pass

    return render(request, "login.html", {"blocked": False})


class Usuario:
    def __init__(self, id_usuario, username):
        self.id_usuario = id_usuario
        self.username = username

    @property
    def valido(self):
        return True

    def username(self):
        return self.username
