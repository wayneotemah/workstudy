# Generated by Django 4.1.3 on 2023-01-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0025_alter_borrowd_asset_options_alter_asset_condition_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowd_asset',
            options={'ordering': ['returned_on'], 'verbose_name': 'Borrowd Asset', 'verbose_name_plural': 'Borrowd Assets'},
        ),
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Good', 'Good'), ('Not Woking', 'Not Working'), ('Faulty', 'Faulty')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Borrowed', 'Borrowed'), ('Not available', ' Not available')], max_length=50, verbose_name='asset status'),
        ),
    ]
