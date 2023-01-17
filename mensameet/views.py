from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TopicsUpdateForm, MeetupCreateForm, MeetupUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Meetup, Topic, Mensa
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
		qs = Meetup.objects.all().order_by('start_time')
		return qs


	def get_context_data(self, **kwargs):
		context = super(MeetupListViewAll, self).get_context_data(**kwargs)
		context.update({'topicsAll': Topic.objects.all().order_by('title'),
			'mensaAll': Mensa.objects.all().order_by('title'),
        	})
		context['b_normal_order'] = True

		return context

	template_name = 'mensameet/home.html'	
	context_object_name = 'meetupsAll'


class MeetupListViewAllReverse(LoginRequiredMixin, ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.all().order_by('-start_time')
		return qs

	def get_context_data(self, **kwargs):
		context = super(MeetupListViewAllReverse, self).get_context_data(**kwargs)
		context.update({'topicsAll': Topic.objects.all().order_by('title'),
			'mensaAll': Mensa.objects.all().order_by('title'),
        	})
		context['b_normal_order'] = True

		return context

	template_name = 'mensameet/home.html'	
	context_object_name = 'meetupsAll'


class MeetupListViewAllGuest(ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.all().order_by('start_time')
		return qs


	def get_context_data(self, **kwargs):
		context = super(MeetupListViewAllGuest, self).get_context_data(**kwargs)
		context.update({'topicsAll': Topic.objects.all().order_by('title'),
			'mensaAll': Mensa.objects.all().order_by('title'),
        	})
		context['b_normal_order'] = True

		return context

	template_name = 'mensameet/home_guest.html'	
	context_object_name = 'meetupsAll'

class MeetupListViewAllGuestReverse(ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.all().order_by('-start_time')
		return qs

	def get_context_data(self, **kwargs):
		context = super(MeetupListViewAllGuestReverse, self).get_context_data(**kwargs)
		context.update({'topicsAll': Topic.objects.all().order_by('title'),
			'mensaAll': Mensa.objects.all().order_by('title'),
			})
		context['b_normal_order'] = True

		return context

	template_name = 'mensameet/home_guest.html'	
	context_object_name = 'meetupsAll'