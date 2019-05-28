from django.shortcuts import render

def login(request):
	return render(request, 'mensameet/login.html')

def home(request):
	return render(request, 'mensameet/home.html')