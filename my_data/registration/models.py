from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='Пользователь')
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name
