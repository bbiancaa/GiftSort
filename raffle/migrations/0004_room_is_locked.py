# Generated by Django 4.0.4 on 2022-08-10 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raffle', '0003_alter_room_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
