# Generated by Django 4.1.3 on 2023-07-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Labs', '0005_alter_issue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Urgent attention', 'Urgent attention'), ('Addressing', 'Addressing'), ('Noted pending address', 'Noted pending address'), ('Low attention', 'Low attention'), ('Medium attention', 'Medium attention'), ('Done', 'Done')], max_length=50, verbose_name='state'),
        ),
    ]
