# Generated by Django 4.1.3 on 2022-12-11 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='day1',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day1_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day1_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day2',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day2_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day2_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day3',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day3_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day3_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day4',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day4_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day4_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day5',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day5_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day5_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day6',
            field=models.CharField(blank=True, choices=[('wednesday', 'Wednesday'), ('Saturday', 'Saturday'), ('monday', 'Monday'), ('Thurday', 'Thursday'), ('Friday', 'Friday'), ('tuesday', 'Tuesday')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day6_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='day6_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
