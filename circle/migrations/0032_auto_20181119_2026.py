# Generated by Django 2.0.5 on 2018-11-19 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0031_auto_20181119_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='user_id',
        ),
        migrations.AddField(
            model_name='like',
            name='nick_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='circle.CircleUser'),
        ),
    ]
