# Generated by Django 3.0.4 on 2020-05-08 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_details',
            new_name='details',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_time',
            new_name='time',
        ),
    ]
