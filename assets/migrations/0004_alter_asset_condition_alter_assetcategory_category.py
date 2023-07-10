# Generated by Django 4.1.3 on 2023-06-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_assetcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Good', 'Good'), ('Not Woking', 'Not Working'), ('Faulty', 'Faulty')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='category',
            field=models.TextField(choices=[('VGA Cables', 'VGA Cables'), ('VGA-HDMI Converters', ' VGA-HDMI Converters'), ('Projector', 'Projector'), ('Others', 'Others'), ('HDMI Cables', 'HDMI Cables')], max_length=50, verbose_name='Asset category name'),
        ),
    ]