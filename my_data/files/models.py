from django.db import models
from registration.models import User
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    
    if hasattr(instance, 'user'):
        return f'files/{ext}/{filename}'
    
    else:
        return f'default_files/{ext}/{filename}'

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    path = models.FileField(upload_to=get_file_path)
    separator = models.CharField(max_length=5)
    has_header = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'
        managed = True
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name
    
class DefaultFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    path = models.FileField(upload_to=get_file_path)
    separator = models.CharField(max_length=5)
    has_header = models.BooleanField()
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'default_files'
        managed = True
        verbose_name = 'Встроенный файл'
        verbose_name_plural = 'Встроенные файлы'

    def __str__(self):
        return self.name
