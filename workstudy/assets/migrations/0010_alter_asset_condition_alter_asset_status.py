# Generated by Django 4.1.3 on 2023-01-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_alter_asset_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Not Woking', 'Not Working'), ('Good', 'Good'), ('Faulty', 'Faulty')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Borrowed', 'Borrowed'), ('Available', 'Available'), ('Not available', ' Not available')], max_length=50, verbose_name='asset status'),
        ),
    ]
