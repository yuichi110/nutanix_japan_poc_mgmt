# Generated by Django 2.2.6 on 2019-11-01 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='complete',
            new_name='finished',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='data',
            new_name='status',
        ),
    ]