# Generated by Django 2.2.1 on 2019-06-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_topic_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='owner',
        ),
        migrations.AddField(
            model_name='profile',
            name='topics',
            field=models.ManyToManyField(related_name='owners', to='users.Topic'),
        ),
    ]