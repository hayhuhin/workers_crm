# Generated by Django 4.1.13 on 2024-02-09 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0005_remove_lead_company_name_lead_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='graph_db',
            field=models.CharField(choices=[('test', 'Test'), ('prod', 'Prod')], default='test', max_length=50),
        ),
    ]
