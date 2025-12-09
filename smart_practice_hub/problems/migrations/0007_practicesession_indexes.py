from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_problem_created_by'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='practicesession',
            index=models.Index(fields=['started_at'], name='practicesession_started_at_idx'),
        ),
        migrations.AddIndex(
            model_name='practicesession',
            index=models.Index(fields=['user', 'started_at'], name='practicesession_user_started_idx'),
        ),
    ]

