# Generated by Django 2.0.5 on 2019-02-03 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0057_auto_20190203_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circleuser',
            old_name='u_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='p_type',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='picture',
        ),
    ]