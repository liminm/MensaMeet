from django.contrib import admin
from .models import Topic
from .models import Meetup
from .models import Profile
from .models import Mensa

admin.site.register(Topic)
admin.site.register(Meetup)
admin.site.register(Profile)
admin.site.register(Mensa)