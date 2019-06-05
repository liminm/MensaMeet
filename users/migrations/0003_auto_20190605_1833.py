# Generated by Django 2.2.1 on 2019-06-05 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190605_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mymeetups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='members',
            field=models.ManyToManyField(related_name='meetupsImin', to=settings.AUTH_USER_MODEL),
        ),
    ]
