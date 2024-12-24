from django.db import models
from registration.models import User
from charts.models import Chart

class Dashboard(models.Model):
    dashboard_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    charts = models.ManyToManyField(Chart, related_name='dashboards')
    created_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'dashboards'
        managed = True
        verbose_name = 'Дашборд'
        verbose_name_plural = 'Дашборды'

    def __str__(self):
        return self.name
