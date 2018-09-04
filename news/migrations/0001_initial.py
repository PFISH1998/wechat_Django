# Generated by Django 2.0.5 on 2018-08-30 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('news_url', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=1000)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
