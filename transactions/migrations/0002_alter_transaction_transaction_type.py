# Generated by Django 4.2.7 on 2023-12-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('DEPOSIT', 'deposit'), ('WITHDRAWAL', 'withdrawal'), ('LOAN', 'loan'), ('LOAN_PAID', 'loan Paid')], max_length=100, null=True),
        ),
    ]
