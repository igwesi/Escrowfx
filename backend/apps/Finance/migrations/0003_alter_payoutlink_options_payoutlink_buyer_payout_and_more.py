# Generated by Django 4.2.11 on 2024-04-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0002_alter_bankaccount_ngn_id_alter_bankaccount_usd_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payoutlink',
            options={'verbose_name_plural': 'Payout Links'},
        ),
        migrations.AddField(
            model_name='payoutlink',
            name='buyer_payout',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='payoutlink',
            name='buyer_payout_destination',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='payoutlink',
            name='seller_payout',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='payoutlink',
            name='seller_payout_destination',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='BankAccount',
        ),
    ]
