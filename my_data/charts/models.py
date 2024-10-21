from django.db import models
from files.models import File
from registration.models import User

class Chart(models.Model):
    chart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    filters = models.JSONField()
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'charts'
        managed = True
        verbose_name = 'Чарт'
        verbose_name_plural = 'Чарты'

    def __str__(self):
        return self.name