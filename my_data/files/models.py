from django.db import models
from registration.models import User

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    separator = models.CharField(max_length=5)
    has_header = models.BooleanField()
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'
        managed = True
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name
