# Generated by Django 4.1.3 on 2023-01-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0020_alter_issue_options_alter_issue_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='scale',
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Argent', 'Argent'), ('Done', 'Done'), ('Pending', 'Pending')], max_length=50, verbose_name='state'),
        ),
    ]