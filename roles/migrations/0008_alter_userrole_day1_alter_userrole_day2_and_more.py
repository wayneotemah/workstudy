# Generated by Django 4.1.3 on 2023-07-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0007_alter_userrole_day1_alter_userrole_day2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='day1',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day2',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day3',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day4',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day5',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day6',
            field=models.CharField(blank=True, choices=[('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Monday', 'Monday'), ('Friday', 'Friday')], max_length=15, null=True),
        ),
    ]
