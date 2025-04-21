from django.db import models

# Create your models here.
from django.db import models

class M_Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Nombre de usuario
    password = models.CharField(max_length=255)  # Contraseña (de preferencia hasheada)

    class Meta:
        db_table = "Usuario"  # Nombre de la tabla en la base de datos
        managed = True  