# Generated by Django 2.0.6 on 2018-08-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_upvoteanswermod'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='q_modified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
