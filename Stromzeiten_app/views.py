from django.shortcuts import render
from .models import Stromzeiten_table

def home(request):
    context = {
        'data': Stromzeiten_table.objects.all().order_by('-Date')
    }
    return render(request, 'Stromzeiten_app/home.html', context)

def about(request):
    return render(request, 'Stromzeiten_app/about.html', {'title': 'About'})

def chart(request):
    context = {
        'data': Stromzeiten_table.objects.order_by('-Date')[:5]
    }
    return render(request, 'Stromzeiten_app/chart.html', context)


