# Generated by Django 4.2.2 on 2023-07-07 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_last_updated_product_last_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
    ]