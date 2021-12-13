from django.db import models
from django.conf import settings

class Usuario(models.Model):
    id_Usuario = models.AutoField(primary_key= True, null=False)
    Nombre = models.CharField(max_length=45, null=False, default='')
    Ap_paterno = models.CharField(max_length=45, null=False, default='')
    Ap_materno = models.CharField(max_length=45, default='')
    Fecha_nacimiento = models.CharField(max_length=45, default='')
    Direccion = models.CharField(max_length=50, default='')
    Telefono = models.CharField(max_length=10, default='')
    Correo = models.EmailField(max_length=50, null=False)
    Contrasena = models.CharField(max_length=45, null=False, default='')

    def __str__(self):
        return self.Nombre

 
class Archivo(models.Model):
    id_Archivo = models.AutoField(primary_key = True, null = False)
    Nombre = models.CharField(max_length = 45, null = False, default = '')
    media = models.FileField(upload_to='myfolder/', blank=True, null=True)
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files', default = 1)

    #     class Meta:
     #       verbose_name = 'Archivo'
      #      verbose_name_plural = 'Archivos'
       #     ordering = ['Nombre']

    def __str__(self):
        return self.Nombre
