# Generated by Django 5.2 on 2025-04-15 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0004_alter_product_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='titletitle',
            new_name='title',
        ),
    ]
