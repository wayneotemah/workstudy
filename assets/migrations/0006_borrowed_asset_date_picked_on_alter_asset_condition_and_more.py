# Generated by Django 4.1.3 on 2023-07-29 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_alter_asset_condition_alter_asset_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowed_asset',
            name='date_picked_on',
            field=models.DateField(default=datetime.date(2023, 7, 29), editable=False, verbose_name='date picked'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Faulty', 'Faulty'), ('Good', 'Good'), ('Not Woking', 'Not Working')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Borrowed', 'Borrowed'), ('Available', 'Available'), ('Pending Approval', 'Pending Approval'), ('Not available', ' Not available')], max_length=50, verbose_name='asset status'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='category',
            field=models.TextField(choices=[('Projector', 'Projector'), ('Remote', 'Remote'), ('HDMI Cables', 'HDMI Cables'), ('VGA Cables', 'VGA Cables'), ('Others', 'Others'), ('VGA-HDMI Converters', ' VGA-HDMI Converters'), ('Extension/Power Cables', 'Extension/Power Cables')], max_length=50, verbose_name='Asset category name'),
        ),
    ]
