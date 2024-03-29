# Generated by Django 4.2.4 on 2023-11-13 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_course_fiche'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='fiche',
            field=models.FileField(null=True, upload_to='fiches_cotation'),
        ),
        migrations.AlterField(
            model_name='student',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.option'),
        ),
        migrations.AlterField(
            model_name='student',
            name='classe_del_eleve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.grade', verbose_name='Classe'),
        ),
    ]
