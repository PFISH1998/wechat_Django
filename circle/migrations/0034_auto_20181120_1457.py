# Generated by Django 2.0.5 on 2018-11-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0033_auto_20181120_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='uid',
        ),
        migrations.AddField(
            model_name='circleuser',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
