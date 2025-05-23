# Generated by Django 5.2 on 2025-04-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0008_alter_contact_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='website',
            new_name='site',
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(db_column='e-mail', max_length=500),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
