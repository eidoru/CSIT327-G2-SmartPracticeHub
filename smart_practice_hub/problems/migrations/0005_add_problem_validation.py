# Generated migration to add unique constraint and indexes to Problem model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_practicesession'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='problem',
            unique_together={('title', 'subject', 'topic')},
        ),
        migrations.AddIndex(
            model_name='problem',
            index=models.Index(fields=['subject', 'difficulty'], name='problems_pr_subject_difficulty_idx'),
        ),
        migrations.AddIndex(
            model_name='problem',
            index=models.Index(fields=['topic'], name='problems_pr_topic_idx'),
        ),
    ]
