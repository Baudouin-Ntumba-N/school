# Generated by Django 4.2.4 on 2023-11-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_alter_course_fiche'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='maximum',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='heures',
            field=models.IntegerField(default=1),
        ),
    ]
