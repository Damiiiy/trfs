# Generated by Django 5.0.6 on 2024-07-30 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examportal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='marks',
            field=models.IntegerField(default=1, max_length=10),
        ),
    ]