# Generated by Django 4.0.4 on 2022-04-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
