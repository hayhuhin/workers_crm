# Generated by Django 4.1.13 on 2024-03-18 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_alter_income_date_received_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='company_name',
        ),
    ]
