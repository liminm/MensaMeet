from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model

from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TopicsUpdateForm, MeetupCreateForm, MeetupUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from django.core.mail import EmailMessage


import os
from .models import Meetup, Topic, Profile, User
from .tokens import account_activation_token
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)

def word2num(word):
	number = {
        'TWO': 2,
        'THREE': 3,
        'FOUR': 4,
        'FIVE': 5,
        'SIX': 6,
        'SEVEN': 7,
        'EIGHT': 8
	}
	return number.get(word, 8)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data['email']
			user.username = form.cleaned_data['username']
			user.password1 = form.cleaned_data['password1']
			user.password2 = form.cleaned_data['password2']
			user.is_active = True
			user.save()
			activateEmail(request, user, form.cleaned_data['email'])
			return redirect('mensameet-home')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form })

def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user is not None and account_activation_token.check_token(user,token):
		user.is_active = True
		user.save()

		messages.success(request, "Thank you for your email confirmation. Now you can login into your account.")
		return redirect('mensameet-login')
	else:
		messages.error(request, "Activation link is invalid!")

	return redirect('mensameet-login')


def activateEmail(request, user, to_email):
	mail_subject = "Activate your user account at MensaMeet."
	message = render_to_string('auth/activate_account.html', {
		'user': user,
		'domain': get_current_site(request).domain,
		'uid':urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol':'https' if request.is_secure() else 'http'
	})
	email = EmailMessage(mail_subject, message, to=[to_email] )
	if email.send():
		messages.success(request, f'Dear {user}, please confirm your account and complete the registration by clicking on the activation link sent to {to_email}.')
	else:
		messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@login_required
def profile(request):

	u_form = UserUpdateForm(instance=request.user)
	p_form = ProfileUpdateForm(instance=request.user.profile)
	t_form = TopicsUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form,
		't_form': t_form
		}
	return render(request, 'users/profile.html', context)



@login_required
def profile_edit(request):
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
	return render(request, 'users/profile_edit.html', context)

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
	if word2num(OurMeetup.members_limit) <= OurMeetup.members.count():
		messages.warning(request, f'{OurMeetup.title} is full!')
	else:
		OurMeetup.members.add(OurUser)
		messages.success(request, f'You have joined {OurMeetup.title}!')
	return redirect('mensameet-home')

@login_required
def deletemyprofile(request):
	OurUser = request.user
	OurUser.delete()
	messages.success(request, f'You have succesfully deleted your account!')
	return redirect('mensameet-login')

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
	success_url = '/mymeetups'

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

# #TODO
# class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# 	model = User
# 	success_url = 'profile-detail'

# 	def test_func(self):
# 		User = self.get_object()
# 		if self.request.user == User:
# 			return True
# 		return False

# class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# 	model = User
# 	success_url = 'profile-detail'

# 	def test_func(self):
# 		User = self.get_object()
# 		if self.request.user == User:
# 			return True
# 		return False


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = User
	success_url = '/login'

	def test_func(self):
		User = self.get_object()
		if self.request.user == User:
			return True
		return False
