# Generated by Django 2.0.5 on 2018-11-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0044_circleuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='circleuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='circleuser',
            name='nick_name',
            field=models.CharField(max_length=120),
        ),
    ]
