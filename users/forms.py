from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Meetup, Topic

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

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
	topics = forms.ModelMultipleChoiceField(
			queryset = Topic.objects.all(),
			widget = forms.CheckboxSelectMultiple,
			required=True
	)

	class Meta:
		model = Meetup
		fields = ['title', 'about', 'start_time', 'topics', 'members_limit', 'mensa']


