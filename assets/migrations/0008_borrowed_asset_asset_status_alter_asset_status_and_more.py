# Generated by Django 4.1.3 on 2023-07-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_merge_20230729_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowed_asset',
            name='asset_status',
            field=models.CharField(blank=True, choices=[('Borrowed', 'Borrowed'), ('Pending Approval', 'Pending Approval'), ('Returned', ' Returned')], max_length=50, null=True, verbose_name='state of the asset'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Borrowed', 'Borrowed'), ('Available', 'Available'), ('Pending Approval', 'Pending Approval'), ('Not available', ' Not available')], max_length=50, verbose_name='asset status'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='category',
            field=models.TextField(choices=[('VGA-HDMI Converters', ' VGA-HDMI Converters'), ('Projector', 'Projector'), ('Extension/Power Cables', 'Extension/Power Cables'), ('Others', 'Others'), ('Remote', 'Remote'), ('VGA Cables', 'VGA Cables'), ('HDMI Cables', 'HDMI Cables')], max_length=50, verbose_name='Asset category name'),
        ),
        migrations.AlterField(
            model_name='borrowed_asset',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
