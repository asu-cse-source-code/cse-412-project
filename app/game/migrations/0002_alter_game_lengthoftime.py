# Generated by Django 4.0.3 on 2022-04-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='LengthOfTime',
            field=models.IntegerField(null=True),
        ),
    ]
