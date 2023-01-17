from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Meetup, Topic, Profile


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', "email", 'password1', 'password2', 'is_active']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'is_active']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']	

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'gender', 'about']

class MeetupCreateForm(forms.ModelForm):
	'''
	topics = forms.ModelMultipleChoiceField(
			queryset = Topic.objects.all(),
			widget = forms.RadioSelect(),
			required=True,
	)
	'''
	class Meta:
		model = Meetup
		fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']

class MeetupUpdateForm(forms.ModelForm):
	'''
	topics = forms.ModelMultipleChoiceField(
			queryset = Topic.objects.all(),
			widget = forms.RadioSelect(),
			required=True,
	)
	'''
	class Meta:
		model = Meetup
		fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']

class TopicsUpdateForm(forms.ModelForm):
	'''
	topics = forms.ModelMultipleChoiceField(
		queryset = Topic.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False
	)
	'''
	class Meta:
		model = Profile
		fields = ['topics']
