# Generated by Django 2.0.5 on 2018-11-27 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0055_auto_20181126_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='circle.Post'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='circle.CircleUser'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='circle.Post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='circle.CircleUser'),
        ),
        migrations.AlterField(
            model_name='post',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='circle.CircleUser'),
        ),
    ]
