from django.db import models
from registration.models import User

class UserSettings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.BooleanField()
    language = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'user_settings'
        managed = True
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'

    def __str__(self):
        return f"Настройки для {self.user.name}"
