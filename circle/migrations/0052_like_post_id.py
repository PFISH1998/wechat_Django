# Generated by Django 2.0.5 on 2018-11-25 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0051_remove_like_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='post_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='circle.Post'),
            preserve_default=False,
        ),
    ]
