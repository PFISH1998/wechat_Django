# Generated by Django 2.0.5 on 2018-11-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0022_auto_20181119_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='circleuser',
            name='nick_name',
            field=models.CharField(max_length=120, primary_key=True, serialize=False, unique=True),
        ),
    ]