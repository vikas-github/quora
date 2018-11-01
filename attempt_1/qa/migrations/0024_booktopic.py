# Generated by Django 2.0.6 on 2018-09-03 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0023_auto_20180903_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_date', models.DateTimeField(verbose_name='Bookmark Date')),
                ('b_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.TopicStore')),
            ],
        ),
    ]