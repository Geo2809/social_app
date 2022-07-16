from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'main/home.html', context)