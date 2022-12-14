# Generated by Django 4.1.3 on 2023-01-02 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_alter_organization_scale'),
        ('assets', '0007_alter_asset_condition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowd_asset',
            options={'verbose_name': 'Borrowd Asset', 'verbose_name_plural': 'Borrowd Assets'},
        ),
        migrations.AlterField(
            model_name='asset',
            name='condition',
            field=models.CharField(choices=[('Faulty', 'Faulty'), ('Not Woking', 'Not Working'), ('Good', 'Good')], max_length=50, verbose_name='asset condition'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='lab / organization'),
        ),
    ]
