# Generated by Django 4.1.3 on 2023-01-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0008_alter_organization_scale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='scale',
            field=models.CharField(choices=[('medium scale', 'medium scale'), ('Small scale', 'Small scale'), ('personal venture', 'personal venture')], max_length=50, verbose_name='Scale of organization'),
        ),
    ]
