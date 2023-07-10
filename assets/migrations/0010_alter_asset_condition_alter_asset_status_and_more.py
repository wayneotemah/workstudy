# Generated by Django 4.1.3 on 2023-07-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_alter_asset_condition_alter_assetcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Good', 'Good'), ('Faulty', 'Faulty'), ('Not Woking', 'Not Working')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Borrowed', 'Borrowed'), ('Not available', ' Not available'), ('Available', 'Available')], max_length=50, verbose_name='asset status'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='category',
            field=models.TextField(choices=[('VGA-HDMI Converters', ' VGA-HDMI Converters'), ('VGA Cables', 'VGA Cables'), ('Others', 'Others'), ('Remote', 'Remote'), ('Projector', 'Projector'), ('HDMI Cables', 'HDMI Cables'), ('Extension/Power Cables', 'Extension/Power Cables')], max_length=50, verbose_name='Asset category name'),
        ),
    ]