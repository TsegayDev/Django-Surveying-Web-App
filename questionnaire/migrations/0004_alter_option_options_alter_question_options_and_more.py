# Generated by Django 5.0.6 on 2024-09-29 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_question_user_questionnaire_user_section_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name_plural': 'Options'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'verbose_name_plural': 'Questionnaires'},
        ),
        migrations.AlterModelOptions(
            name='response',
            options={'verbose_name_plural': 'Responses'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name_plural': 'Sections'},
        ),
    ]
