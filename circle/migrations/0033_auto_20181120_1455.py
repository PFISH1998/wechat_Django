# Generated by Django 2.0.5 on 2018-11-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0032_auto_20181119_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='user',
        ),
        migrations.AddField(
            model_name='circleuser',
            name='uid',
            field=models.IntegerField(auto_created=True, default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='circleuser',
            name='nick_name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]