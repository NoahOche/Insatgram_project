# Generated by Django 4.1.7 on 2024-12-08 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_message_created_alter_message_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]
