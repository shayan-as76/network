# Generated by Django 5.0 on 2024-11-24 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='like',
            field=models.BooleanField(default=False, verbose_name='like'),
        ),
    ]
