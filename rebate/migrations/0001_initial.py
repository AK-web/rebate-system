# Generated by Django 5.1.4 on 2024-12-13 20:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RebateProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(help_text='Unique name of the rebate program', max_length=200, unique=True)),
                ('rebate_percentage', models.DecimalField(decimal_places=2, help_text='Percentage of rebate offered (0-100%)', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField(help_text='Start date of the rebate program')),
                ('end_date', models.DateField(help_text='End date of the rebate program')),
                ('eligibility_criteria', models.TextField(blank=True, help_text='Detailed description of program eligibility', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Whether the rebate program is currently active')),
            ],
            options={
                'verbose_name_plural': 'Rebate Programs',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(help_text='Unique identifier for the transaction', max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Total transaction amount', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('transaction_date', models.DateTimeField(help_text='Date and time of the transaction')),
                ('rebate_program', models.ForeignKey(help_text='Rebate program associated with this transaction', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='rebate.rebateprogram')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'ordering': ['-transaction_date'],
            },
        ),
        migrations.CreateModel(
            name='RebateClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_id', models.CharField(help_text='Unique identifier for the rebate claim', max_length=100, unique=True)),
                ('claim_amount', models.DecimalField(decimal_places=2, help_text='Amount of rebate claimed', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('claim_status', models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', help_text='Current status of the rebate claim', max_length=20)),
                ('claim_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when the claim was submitted')),
                ('notes', models.TextField(blank=True, help_text='Additional notes or reason for claim status', null=True)),
                ('transaction', models.OneToOneField(help_text='Transaction associated with this claim', on_delete=django.db.models.deletion.CASCADE, related_name='rebate_claim', to='rebate.transaction')),
            ],
            options={
                'verbose_name_plural': 'Rebate Claims',
                'ordering': ['-claim_date'],
            },
        ),
    ]