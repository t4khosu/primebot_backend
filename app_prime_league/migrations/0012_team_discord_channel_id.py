# Generated by Django 3.0.8 on 2021-03-09 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_prime_league', '0011_auto_20210308_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='discord_channel_id',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
