# Generated by Django 5.2 on 2025-04-30 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0019_cart_cartitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'managed': True, 'verbose_name': 'Cart', 'verbose_name_plural': 'Carts'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'managed': True, 'verbose_name': 'CartItem', 'verbose_name_plural': 'CartItems'},
        ),
        migrations.AlterModelTable(
            name='cart',
            table='Cart',
        ),
        migrations.AlterModelTable(
            name='cartitem',
            table='CartItem',
        ),
    ]
