from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import M_Usuario
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
        
        print(username, password)
        ##aqui el codigo respecto al la validacion en la BD
        #query = "EXEC sp_validarUsuario @id = %s, @username = %s, @password = %s"
        #resultado = M_Usuario.objects.raw(query, ['7',username, password])
        #print(list(resultado)[0]if resultado else None)
        

        #simulacion de validacion de usuario
        if username == "admin" and password == "pass":
            if is_ajax:
                return JsonResponse({"success": True, "username": username, "redirect": "home"})
            return redirect("home")
        else:
            if is_ajax:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")
