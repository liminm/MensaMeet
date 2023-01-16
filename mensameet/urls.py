from django.urls import path
from mensameet.views import (
MeetupListViewAll,
MeetupListViewAllReverse,
)

urlpatterns = [
    path('', MeetupListViewAll.as_view(), name='mensameet-home'),
    path('reverse', MeetupListViewAllReverse.as_view(), name='mensameet-home-reverse'),

]
