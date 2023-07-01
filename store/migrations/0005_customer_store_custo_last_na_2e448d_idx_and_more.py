# Generated by Django 4.2.2 on 2023-07-01 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_zip'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name', 'first_name'], name='store_custo_last_na_2e448d_idx'),
        ),
        migrations.AlterModelTable(
            name='customer',
            table='store_customer',
        ),
    ]