# Generated by Django 3.2.9 on 2021-12-03 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('LOW', 'low'), ('MEDIUM', 'medium'), ('HIGH', 'high')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('TODO', 'todo'), ('IN PROGRESS', 'in progress'), ('DONE', 'done')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('BUG', 'bug'), ('IMPROVEMENT ', 'improvement'), ('TASK', 'task')], max_length=128),
        ),
    ]