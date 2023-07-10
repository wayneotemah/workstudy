# Generated by Django 4.1.3 on 2023-06-07 11:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('Lab_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name="Lab's ID")),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Lab name')),
                ('supervisor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Lab', to='accounts.account', verbose_name="Lab's creater")),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title of the field')),
                ('details', models.TextField(max_length=400, verbose_name='issue details')),
                ('reported_on', models.DateTimeField(verbose_name='date reported')),
                ('status', models.CharField(choices=[('Noted pending address', 'Noted pending address'), ('Low attention', 'Low attention'), ('Urgent attention', 'Urgent attention'), ('Medium attention', 'Medium attention'), ('Done', 'Done'), ('Addressing', 'Addressing')], max_length=50, verbose_name='state')),
                ('admin_response', models.TextField(blank=True, null=True, verbose_name='admins responses ')),
                ('Lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Labs.lab', verbose_name='Lab')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account', verbose_name='reported_by')),
            ],
            options={
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
                'ordering': ['-reported_on'],
            },
        ),
    ]