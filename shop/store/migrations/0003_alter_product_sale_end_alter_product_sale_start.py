# Generated by Django 4.2.4 on 2023-09-06 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_sale_end_alter_product_sale_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_end',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_start',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
