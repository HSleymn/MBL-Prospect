# Generated by Django 5.2 on 2025-04-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0011_rename_businessstatus_contact_business_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='business_status',
            new_name='businessstatus',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='postal_code',
            new_name='postalcode',
        ),
        migrations.AlterField(
            model_name='contact',
            name='site',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
