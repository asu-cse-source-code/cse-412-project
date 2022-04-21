# Generated by Django 4.0.3 on 2022-04-21 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_game_console'),
        ('award', '0002_alter_award_game_alter_award_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='Game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Awards', to='game.game'),
        ),
    ]