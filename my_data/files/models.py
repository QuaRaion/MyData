from django.db import models
from django.urls import reverse
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    name = models.CharField(max_length=50)
    path = models.FileField(upload_to='files/')
    separator = models.CharField(max_length=5)
    has_header = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)


    class Meta:
        db_table = 'files'
        managed = True
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('create_chart', kwargs={'file_id' : self.pk})
