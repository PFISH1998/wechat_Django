# Generated by Django 2.0.5 on 2018-11-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circleuser',
            name='date_join',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
