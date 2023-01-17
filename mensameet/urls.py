from django.urls import path
from mensameet.views import (
MeetupListViewAll,
MeetupListViewAllReverse,
MeetupListViewAllGuest,
MeetupListViewAllGuestReverse,
)

urlpatterns = [
    path('', MeetupListViewAll.as_view(), name='mensameet-home'),
    path('reverse', MeetupListViewAllReverse.as_view(), name='mensameet-home-reverse'),
    path('guest', MeetupListViewAllGuest.as_view(), name='mensameet-home-guest'),
    path('guest-reverse', MeetupListViewAllGuestReverse.as_view(), name='mensameet-home-guest-reverse'),  
]
