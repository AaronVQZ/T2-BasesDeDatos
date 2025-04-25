from django.contrib import admin
from django.urls import path, include
from appLogin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('login/', include('appLogin.urls')),
    path('home/', include('empleados.urls', namespace='empleados') ),
]

