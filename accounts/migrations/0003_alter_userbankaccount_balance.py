# Generated by Django 4.2.7 on 2023-12-28 14:16

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_useraddress_user_alter_userbankaccount_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12),
        ),
    ]