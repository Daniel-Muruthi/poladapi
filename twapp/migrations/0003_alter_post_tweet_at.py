# Generated by Django 3.2.9 on 2021-11-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twapp', '0002_alter_post_tweet_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tweet_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
