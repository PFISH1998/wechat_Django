# Generated by Django 2.0.5 on 2018-11-19 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0020_auto_20181119_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circleuser',
            old_name='user',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='circleuser',
            name='nick_name',
            field=models.CharField(max_length=120, primary_key=True, unique=True),
        ),
    ]
