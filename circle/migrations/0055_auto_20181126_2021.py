# Generated by Django 2.0.5 on 2018-11-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0054_auto_20181126_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='status',
            field=models.BooleanField(),
        ),
    ]
