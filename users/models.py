from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Topic(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Meetup(models.Model):
    title = models.CharField(max_length=100)
    #many to many relationship between topics and meetups 
    topic = models.ManyToManyField(Topic)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    #one to many relationship between meetups and users
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #members

    def __str__(self):
        return self.title
