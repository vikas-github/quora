# Generated by Django 2.0.6 on 2018-08-11 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_auto_20180811_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteanswermod',
            name='action_taken',
            field=models.SmallIntegerField(),
        ),
    ]
