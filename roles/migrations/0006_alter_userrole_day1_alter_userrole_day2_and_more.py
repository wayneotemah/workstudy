# Generated by Django 4.1.3 on 2023-06-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0005_alter_userrole_day1_alter_userrole_day2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='day1',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day2',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day3',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day4',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day5',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='day6',
            field=models.CharField(blank=True, choices=[('Wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('Thurday', 'Thursday'), ('Tuesday', 'Tuesday'), ('Friday', 'Friday'), ('Monday', 'Monday')], max_length=15, null=True),
        ),
    ]
