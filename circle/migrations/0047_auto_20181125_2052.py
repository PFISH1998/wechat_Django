# Generated by Django 2.0.5 on 2018-11-25 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0046_auto_20181125_1706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='nick_name',
            new_name='uid',
        ),
        migrations.AlterField(
            model_name='comments',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='circle.CircleUser'),
        ),
    ]