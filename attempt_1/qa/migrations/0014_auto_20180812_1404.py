# Generated by Django 2.0.6 on 2018-08-12 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0013_auto_20180812_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answercomment',
            name='comment_date',
        ),
        migrations.RemoveField(
            model_name='answercomment',
            name='comment_user',
        ),
    ]