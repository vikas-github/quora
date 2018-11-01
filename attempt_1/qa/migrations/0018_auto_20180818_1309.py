# Generated by Django 2.0.6 on 2018-08-18 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0017_bookmarkquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_date', models.DateTimeField(verbose_name='Bookmark Date')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Answer')),
                ('b_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='bookmarkquestion',
            name='b_user',
        ),
        migrations.RemoveField(
            model_name='bookmarkquestion',
            name='question',
        ),
        migrations.DeleteModel(
            name='BookmarkQuestion',
        ),
    ]