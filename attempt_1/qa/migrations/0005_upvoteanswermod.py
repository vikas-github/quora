# Generated by Django 2.0.6 on 2018-07-14 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0004_auto_20180711_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpvoteAnswerMod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvote_date', models.DateTimeField(verbose_name='Date Upvoted')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Answer')),
                ('upvote_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
