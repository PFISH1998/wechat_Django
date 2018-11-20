# Generated by Django 2.0.5 on 2018-11-18 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0007_auto_20181118_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circleuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='circleuser',
            name='nick_name',
            field=models.CharField(max_length=120, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='circle.CircleUser'),
        ),
        migrations.AlterField(
            model_name='post',
            name='nick_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.CircleUser'),
        ),
    ]