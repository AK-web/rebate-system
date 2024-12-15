# Generated by Django 5.1.4 on 2024-12-14 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rebate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rebateclaim',
            name='claim_id',
            field=models.CharField(blank=True, help_text='Unique identifier for the rebate claim', max_length=100, null=True),
        ),
    ]
