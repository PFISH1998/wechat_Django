# Generated by Django 2.0.5 on 2018-11-19 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0029_auto_20181119_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='circleuser',
            name='user',
            field=models.IntegerField(auto_created=True, default=1),
            preserve_default=False,
        ),
    ]
