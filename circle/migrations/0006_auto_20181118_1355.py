# Generated by Django 2.0.5 on 2018-11-18 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0005_auto_20181118_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_time']},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='content',
            new_name='comment_content',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='pub_time',
            new_name='comment_time',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='post',
            new_name='post_id',
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='circle.CircleUser', to_field='nick_name'),
        ),
    ]