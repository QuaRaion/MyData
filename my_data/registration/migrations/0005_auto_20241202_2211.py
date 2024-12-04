# Generated by Django 5.1.2 on 2024-12-02 19:11

from django.db import migrations

def update_admin_log_user(apps, schema_editor):
    AdminLog = apps.get_model('admin', 'LogEntry')
    User = apps.get_model('registration', 'User')

    AdminLog.objects.filter(user__isnull=False).update(user=None)

class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RunPython(update_admin_log_user),
    ]
