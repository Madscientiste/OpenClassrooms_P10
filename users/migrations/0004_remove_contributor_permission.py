# Generated by Django 3.2.9 on 2022-01-20 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_contributor_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='permission',
        ),
    ]
