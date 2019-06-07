from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile ,self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)    
        

class Topic(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Meetup(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default = timezone.now)
    #many to many relationship between topics and meetups 
    topic = models.ManyToManyField(Topic)
    about = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default = timezone.now)
    #one to many relationship between meetups and users
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mymeetups")
    members = models.ManyToManyField(User, related_name="meetupsImin")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meetup-detail', kwargs={'pk': self.pk})    
