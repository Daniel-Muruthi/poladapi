# Generated by Django 3.2.9 on 2021-11-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twapp', '0003_alter_post_tweet_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tweet_at',
            field=models.DateTimeField(null=True),
        ),
    ]
