# Generated by Django 5.0.6 on 2024-08-05 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examportal', '0003_alter_question_marks'),
        ('resultapp', '0002_alter_student_result_exam_scores_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_result',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examportal.exam'),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='total_scores',
            field=models.IntegerField(editable=False),
        ),
    ]
