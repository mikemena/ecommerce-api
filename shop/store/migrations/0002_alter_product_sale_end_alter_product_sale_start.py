# Generated by Django 4.2.4 on 2023-09-06 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_end',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_start',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
