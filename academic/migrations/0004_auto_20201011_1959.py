# Generated by Django 3.0.7 on 2020-10-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_auto_20201002_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situacao_aluno',
            name='nota',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
