# Generated by Django 4.2.11 on 2024-04-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_business_name_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(choices=[('Australia', 'AU'), ('Canada', 'CA'), ('Ghana', 'GH'), ('Nigeria', 'NG'), ('United States', 'US')], max_length=50, verbose_name='Country Codes e.g US, NG'),
        ),
    ]