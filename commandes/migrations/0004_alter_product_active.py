# Generated by Django 5.2 on 2025-04-15 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0003_alter_product_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
