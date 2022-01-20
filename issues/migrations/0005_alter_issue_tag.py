# Generated by Django 3.2.9 on 2022-01-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_remove_issue_assignee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('BUG', 'bug'), ('IMPROVEMENT', 'improvement'), ('TASK', 'task')], max_length=128),
        ),
    ]