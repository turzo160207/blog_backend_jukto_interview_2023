# Generated by Django 4.1.7 on 2023-03-25 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_post_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-views']},
        ),
        migrations.DeleteModel(
            name='PostView',
        ),
    ]
