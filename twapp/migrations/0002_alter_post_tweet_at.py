# Generated by Django 3.2.9 on 2021-11-18 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tweet_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
