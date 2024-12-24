from django.apps import AppConfig


class ChartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charts'
    
    # функция для подключения dash приложения
    # def ready(self): 
    #     import charts.dash_apps

