# Generated by Django 4.1.3 on 2023-01-06 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_alter_organization_scale'),
        ('assets', '0015_alter_asset_condition_alter_asset_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Not available', ' Not available'), ('Borrowed', 'Borrowed')], max_length=50, verbose_name='asset status'),
        ),
        migrations.AlterField(
            model_name='borrowd_asset',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='lab'),
        ),
    ]