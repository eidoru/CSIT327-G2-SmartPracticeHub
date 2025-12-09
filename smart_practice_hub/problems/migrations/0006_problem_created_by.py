from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_add_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                help_text='Teacher who authored the problem',
                null=True,
                on_delete=models.CASCADE,
                related_name='problems_created',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

