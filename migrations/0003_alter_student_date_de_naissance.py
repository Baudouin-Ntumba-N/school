# Generated by Django 4.2.4 on 2023-11-10 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_prof_options_alter_student_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_de_naissance',
            field=models.DateField(null=True),
        ),
    ]