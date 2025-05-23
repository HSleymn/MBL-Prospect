# Generated by Django 5.2 on 2025-04-30 15:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0011_alter_offer_idproduct_alter_offer_price_and_more'),
        ('utilisateurs', '0018_alter_users_mailbalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='utilisateurs.cart')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commandes.offer')),
            ],
            options={
                'unique_together': {('cart', 'offer')},
            },
        ),
    ]
