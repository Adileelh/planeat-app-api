# Generated by Django 4.0.10 on 2023-07-12 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]