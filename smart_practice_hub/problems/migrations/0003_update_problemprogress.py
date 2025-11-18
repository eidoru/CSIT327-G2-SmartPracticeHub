# Generated migration to fix ProblemProgress model fields

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_problemprogress'),
    ]

    operations = [
        # Remove the old incorrect field
        migrations.RemoveField(
            model_name='problemprogress',
            name='last_attempted',
        ),
        migrations.RemoveField(
            model_name='problemprogress',
            name='started_at',
        ),
        
        # Add the correct fields
        migrations.AddField(
            model_name='problemprogress',
            name='student_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problemprogress',
            name='first_attempted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='problemprogress',
            name='last_attempted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='problemprogress',
            name='time_spent',
            field=models.IntegerField(default=0, help_text='Time spent in seconds'),
        ),
        
        # Update Meta options
        migrations.AlterModelOptions(
            name='problemprogress',
            options={
                'ordering': ['-last_attempted_at'],
                'verbose_name': 'Problem Progress',
                'verbose_name_plural': 'Problem Progress'
            },
        ),
        migrations.AlterUniqueTogether(
            name='problemprogress',
            unique_together={('student', 'problem')},
        ),
    ]
