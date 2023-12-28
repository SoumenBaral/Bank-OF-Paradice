# Generated by Django 4.2.7 on 2023-12-28 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'deposit'), (2, 'withdrawal'), (3, 'loan'), (4, 'loan Paid')], null=True),
        ),
    ]