from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TopicsUpdateForm, MeetupCreateForm, MeetupUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meetup, Topic, Profile
import os
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.email = form.cleaned_data['email']
			post.username = form.cleaned_data['username']
			post.password1 = form.cleaned_data['password1']
			post.password2 = form.cleaned_data['password2']

			post.save()
			messages.success(request, 'Account successfully created')
			return redirect('mensameet-home')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form })


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		t_form = TopicsUpdateForm(request.POST, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid() and t_form.is_valid():
			u_form.save()
			p_form.save()
			t_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		t_form = TopicsUpdateForm(instance=request.user.profile)
	
	context = {
		'u_form': u_form,
		'p_form': p_form,
		't_form': t_form
		}	
	return render(request, 'users/profile.html', context)	

class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = Profile

@login_required
def leaveMeetup(request, pk):
	OurUser = request.user
	OurMeetup = OurUser.meetups_i_am_in.get(id=pk)
	OurMeetup.members.remove(OurUser)
	if OurMeetup.author == OurUser:
		if OurMeetup.members.exists():
			OurMeetup.author = OurMeetup.members.all()[0]
			OurMeetup.save()	
		else:
			OurMeetup.delete()			
	messages.success(request, f'You have left {OurMeetup.title}!')
	return redirect('mensameet-home')

@login_required
def joinMeetup(request, pk):
	OurUser = request.user
	OurMeetup = Meetup.objects.get(id=pk)
	OurMeetup.members.add(OurUser)
	messages.success(request, f'You have joined {OurMeetup.title}!')
	return redirect('mensameet-home')

class MeetupListView(LoginRequiredMixin, ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.filter(author=self.request.user)
		return qs

	template_name = 'users/ownmeetups.html'	
	context_object_name = 'meetups'
	ordering = ['-date_posted']

class MeetupDetailView(LoginRequiredMixin, DetailView):
	model = Meetup

class MeetupCreateView(LoginRequiredMixin, CreateView):
	model = Meetup
	fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']
	success_url = '/mymeetups'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.save()
		form.instance.members.add(self.request.user)
		return super().form_valid(form)		

	def get_context_data(self, **kwargs):
		context = super(MeetupCreateView, self).get_context_data(**kwargs)

		form = MeetupCreateForm(self.request.POST or None)
		context["form"] = form	

		return context


class MeetupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Meetup
	fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		meetup = self.get_object()
		if self.request.user == meetup.author:
			return True
		return False
		
	def get_context_data(self, **kwargs):
		context = super(MeetupUpdateView, self).get_context_data(**kwargs)
		form = MeetupUpdateForm(instance=self.get_object())
		context["form"] = form
		return context


class MeetupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Meetup
	success_url = '/mymeetups'

	def test_func(self):
		meetup = self.get_object()
		if self.request.user == meetup.author:
			return True
		return False

def email(request):
	subject = 'Thank you for changing your password'
	message = ' it  means a world to us '
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [{{ email }},]
	send_mail( subject, message, email_from, recipient_list)
	return redirect('password_reset_done')			