# Generated by Django 2.0.6 on 2018-08-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0009_auto_20180811_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='lname',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='short_bio',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]
