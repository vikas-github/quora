# Generated by Django 2.0.6 on 2018-08-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0010_auto_20180812_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='site_media/'),
        ),
    ]