# Generated by Django 2.0.5 on 2018-11-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0034_auto_20181120_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='id',
        ),
        migrations.AddField(
            model_name='circleuser',
            name='uid',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
