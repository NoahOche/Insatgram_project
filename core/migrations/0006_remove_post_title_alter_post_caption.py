# Generated by Django 4.2.2 on 2023-10-30 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_comment_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(max_length=200),
        ),
    ]
