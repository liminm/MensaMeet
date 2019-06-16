from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TopicsUpdateForm, MeetupCreateForm, MeetupUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Meetup, Topic
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

@login_required
def home(request):
	return render(request, 'mensameet/home.html')

class MeetupListViewAll(LoginRequiredMixin, ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.all()
		return qs

	template_name = 'mensameet/home.html'	
	context_object_name = 'meetupsAll'
	ordering = ['-date_posted']
