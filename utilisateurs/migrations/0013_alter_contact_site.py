# Generated by Django 5.2 on 2025-04-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0012_rename_business_status_contact_businessstatus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='site',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
