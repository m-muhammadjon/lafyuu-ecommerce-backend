# Generated by Django 3.2.5 on 2022-01-08 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_top',
            field=models.BooleanField(default=True),
        ),
    ]