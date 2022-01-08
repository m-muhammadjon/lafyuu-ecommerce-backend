# Generated by Django 3.2.5 on 2021-12-12 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20211211_1447'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MainCategory',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='shop.category'),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
