# Generated by Django 2.0.5 on 2018-11-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0036_auto_20181120_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circleuser',
            name='uid',
            field=models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False),
        ),
    ]
