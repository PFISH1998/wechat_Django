# Generated by Django 2.0.5 on 2018-11-25 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0047_auto_20181125_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='circle.CircleUser'),
        ),
    ]
