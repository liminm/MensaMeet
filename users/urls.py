from django.urls import path
from . import views
from .views import (
    MeetupListView,
    MeetupDetailView,
    MeetupCreateView,
    MeetupUpdateView,
    MeetupDeleteView,
    ProfileDetailView,
    #ProfileEditView,
    ProfileDeleteView
)

urlpatterns = [
    path('', MeetupListView.as_view(), name='meetup-home'),
    path('meetup/<int:pk>/', MeetupDetailView.as_view(), name='meetup-detail'),
    path('meetup/new/', MeetupCreateView.as_view(), name='meetup-create'),
    path('meetup/<int:pk>/update/', MeetupUpdateView.as_view(), name='meetup-update'),
    path('meetup/<int:pk>/delete/', MeetupDeleteView.as_view(), name='meetup-delete'),
    path('meetup/<int:pk>/leave/', views.leaveMeetup, name='leave_meetup'),
    path('meetup/<int:pk>/join/', views.joinMeetup, name='join_meetup'),
    path('user/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    #path('user/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),

    path('user/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]