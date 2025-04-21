from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect
#from .models import M_Usuario
import json


def login(request):
    if request.method == "POST":
        # verifica si la peticion es ajax
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # manejo de datos json o form
        if is_ajax:
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            username = request.POST.get("username",'')
            password = request.POST.get("password",'')
        

        query = "EXEC sp_validarUsuario ?, ?"
        connection.ensure_connection()
        conn = connection.connection

        #la bd devuelve un 1 si el usuario existe y 0 si no existe
        codError = conn.execute(query,(username,password)).fetchone()[0]
        
        if codError == 1:
            if is_ajax:
                return JsonResponse({"success": True, "username": username, "redirect": "home"})
            return redirect("home")
        else:
            if is_ajax:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
            return render(request, "login.html", {"error": "Invalid credentials"})
        
    return render(request, "login.html")
