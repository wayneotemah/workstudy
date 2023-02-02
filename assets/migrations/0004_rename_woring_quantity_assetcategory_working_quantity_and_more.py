# Generated by Django 4.1.3 on 2023-02-02 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_remove_assetcategory_categorty_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetcategory',
            old_name='woring_quantity',
            new_name='working_quantity',
        ),
        migrations.AddField(
            model_name='assetcategory',
            name='borrowed_assets',
            field=models.PositiveIntegerField(default=0, verbose_name='number is assets that are borrowedd'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Faulty', 'Faulty'), ('Not Woking', 'Not Working'), ('Good', 'Good')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Not available', ' Not available'), ('Available', 'Available'), ('Borrowed', 'Borrowed')], max_length=50, verbose_name='asset status'),
        ),
    ]