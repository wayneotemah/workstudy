# Generated by Django 4.1.3 on 2023-01-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0028_alter_issue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('Argent', 'Argent')], max_length=50, verbose_name='state'),
        ),
    ]