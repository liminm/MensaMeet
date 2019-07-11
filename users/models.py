from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from time import strftime, gmtime
from datetime import date
from datetime import datetime



class Topic(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='mensameet/static')
    gender = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, related_name="owners")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile ,self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Mensa(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Meetup(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)

    date_posted = models.DateTimeField(default = timezone.now)
    start_time = models.DateTimeField(default = timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_meetups")
    # has
    topics = models.ManyToManyField(Topic)
    # joined by
    members = models.ManyToManyField(User, related_name="meetups_i_am_in")

    MEMBERS_LIMIT_CHOICES = [
        ('TWO',   '2'),
        ('THREE', '3'),
        ('FOUR',  '4'),
        ('FIVE',  '5'),
        ('SIX',   '6'),
        ('SEVEN', '7'),
        ('EIGHT', '8')
    ]
    members_limit = models.CharField(max_length=5, choices=MEMBERS_LIMIT_CHOICES, default='FOUR')

    # takes place in
    mensa = models.ForeignKey(Mensa, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meetup-detail', kwargs={'pk': self.pk})

    def cur_date(self):

        return datetime.now()
