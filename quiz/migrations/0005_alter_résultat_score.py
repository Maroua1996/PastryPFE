# Generated by Django 4.2.5 on 2023-09-07 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quiz_description_alter_résultat_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='résultat',
            name='score',
            field=models.FloatField(),
        ),
    ]
