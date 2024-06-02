from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Meetup, Topic, Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'email', 'password1', 'password2', 'is_active']:
			self.fields[fieldname].help_text = None

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('This email address is already in use.'
											'\nPlease use a different email address.')
		return email
		


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

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('image', css_class='custom-css-class'),
            Field('gender', css_class='custom-css-class'),
            Field('about', css_class='custom-css-class'),
        )
        
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
	topics = forms.ModelMultipleChoiceField(
		queryset=Topic.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False
	)	


	class Meta:
		model = Profile
		fields = ['topics']
		
