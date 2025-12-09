from django.db import migrations, models


def copy_solution_to_correct_answer(apps, schema_editor):
    Problem = apps.get_model('problems', 'Problem')
    for problem in Problem.objects.all():
        if not problem.correct_answer:
            problem.correct_answer = problem.solution or ''
            problem.save(update_fields=['correct_answer'])


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_practicesession'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='correct_answer',
            field=models.TextField(blank=True, default='', help_text='Exact answer used for auto-grading'),
        ),
        migrations.RunPython(copy_solution_to_correct_answer, migrations.RunPython.noop),
    ]

