from django.urls import path
from mensameet.views import (
MeetupListViewAll
)

urlpatterns = [
    path('', MeetupListViewAll.as_view(), name='mensameet-home'),
]
