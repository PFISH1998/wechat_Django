# Generated by Django 2.0.5 on 2018-11-17 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0003_auto_20181117_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='user',
        ),
    ]