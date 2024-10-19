from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='Пользователь')
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    created_time = models.DateTimeField()

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return self.name


class Dashboard(models.Model):
    dashboard_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_time = models.DateTimeField()

    class Meta:
        db_table = 'dashboards'
        managed = True

    def __str__(self):
        return self.name

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    separator = models.CharField(max_length=5)
    has_header = models.BooleanField()
    created_time = models.DateTimeField()

    class Meta:
        db_table = 'files'
        managed = True

    def __str__(self):
        return self.name


class Chart(models.Model):
    chart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    filters = models.JSONField()

    class Meta:
        db_table = 'charts'
        managed = True

    def __str__(self):
        return self.name

class DashboardChart(models.Model):
    relation_id = models.AutoField(primary_key=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)

    class Meta:
        db_table = 'dashboards_charts'
        managed = True

    def __str__(self):
        return f"Отношение: {self.dashboard.name} - {self.chart.name}"

class UserSettings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.BooleanField()
    language = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'user_settings'
        managed = True

    def __str__(self):
        return f"Настройки для {self.user.name}"
