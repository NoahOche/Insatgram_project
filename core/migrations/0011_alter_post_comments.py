# Generated by Django 4.2.2 on 2023-11-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='comments', to='core.comment'),
        ),
    ]
