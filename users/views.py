from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TopicsUpdateForm, MeetupCreateForm, MeetupUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meetup, Topic
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
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
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

@login_required
def leaveMeetup(request, pk):
	OurUser = request.user
	#OurMeetup = OurUser.my_meetups.get(id=pk)
	OurMeetup = OurUser.meetups_i_am_in.get(id=pk)
	OurMeetup.members.remove(OurUser)
	#OurUser.my_meetups.remove(OurMeetup)
	if OurMeetup.author == OurUser:
		OurMeetup.delete()
	messages.success(request, f'You have left this meetup! {OurMeetup.author}')
	return render(request, 'users/ownmeetups.html')

@login_required
def joinMeetup(request, pk):
	OurUser = request.user
	OurMeetup = Meetup.objects.get(id=pk)
	OurMeetup.members.add(OurUser)
	messages.success(request, f'You have joined in this meetup!')
	return render(request, 'users/ownmeetups.html')

class MeetupListView(LoginRequiredMixin, ListView):
	model = Meetup

	def get_queryset(self):
		qs = Meetup.objects.filter(author=self.request.user)
		return qs

	template_name = 'users/ownmeetups.html'	
	context_object_name = 'meetups'
	ordering = ['-date_posted']

class MeetupDetailView(DetailView):
	model = Meetup


class MeetupCreateView(LoginRequiredMixin, CreateView):
	model = Meetup
	fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']
	success_url = '/mymeetups'
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


#class MeetupCreateView(TemplateView):
#	template_name = "users/meetup_form.html"
#
#	def post(self, request, *args, **kwargs):
#		context = self.get_context_data()
#		if context["form"].is_valid():
#			print ('yes done')
#			form = context["form"]
#			form.instance.author = self.request.user
#			#meetup = form.save(commit = False)
#			#meetup.save()
#			for topic in Topic.objects.all():
#				print(topic)
#				#meetup.topic_set.add(topic)
#			form.save()
#
#		return super(TemplateView, self).render_to_response(context)

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
		