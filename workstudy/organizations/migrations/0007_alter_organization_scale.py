# Generated by Django 4.1.3 on 2023-01-02 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_alter_organization_scale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='scale',
            field=models.CharField(choices=[('Small scale', 'Small scale'), ('personal venture', 'personal venture'), ('medium scale', 'medium scale')], max_length=50, verbose_name='Scale of organization'),
        ),
    ]