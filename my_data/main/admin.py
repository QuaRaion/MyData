from django.contrib import admin
from .models import User, File, Chart, Dashboard, DashboardChart, UserSettings 

admin.site.register(User)
admin.site.register(File)
admin.site.register(Chart)
admin.site.register(Dashboard)
admin.site.register(DashboardChart)
admin.site.register(UserSettings)
