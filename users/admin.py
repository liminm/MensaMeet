from django.contrib import admin
from .models import Topic
from .models import Meetup
from .models import Profile

admin.site.register(Topic)
admin.site.register(Meetup)
admin.site.register(Profile)