# Generated by Django 4.1.3 on 2023-01-09 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('organizations', '0030_remove_issue_reported_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='reported_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.account', verbose_name='reported_by'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Argent', 'Argent'), ('Pending', 'Pending'), ('Done', 'Done')], max_length=50, verbose_name='state'),
        ),
    ]
