# Generated by Django 2.2.1 on 2019-06-21 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190612_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='meetup',
            old_name='date',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='meetup',
            old_name='topic',
            new_name='topics',
        ),
        migrations.AddField(
            model_name='meetup',
            name='members_limit',
            field=models.CharField(choices=[('TWO', '2'), ('THREE', '3'), ('FOUR', '4'), ('FIVE', '5'), ('SIX', '6'), ('SEVEN', '7'), ('EIGHT', '8')], default='FOUR', max_length=5),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_meetups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='members',
            field=models.ManyToManyField(related_name='meetups_i_am_in', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meetup',
            name='mensa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Mensa'),
        ),
    ]