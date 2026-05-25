from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_onboarding_completed_customuser_questionnaire_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(
                choices=[
                    ('student', 'Studente'),
                    ('teacher', 'Docente'),
                    ('teamleader', 'Team Leader'),
                    ('admin', 'Admin'),
                ],
                default='student',
                max_length=20,
            ),
        ),
    ]
