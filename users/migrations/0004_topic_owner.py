# Generated by Django 2.2.1 on 2019-06-12 18:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20190605_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='owner',
            field=models.ManyToManyField(related_name='topicsIown', to=settings.AUTH_USER_MODEL),
        ),
    ]
