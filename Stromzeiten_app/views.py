from django.shortcuts import render
from .models import Stromzeiten_table
from datetime import datetime

now = datetime.now()

def home(request):
    for items in Stromzeiten_table.objects.all():
        if items.Quality_ratio == 100:
            context = {
              'data': Stromzeiten_table.objects.order_by('Date')
                 }
        else:
            print("nothing")
    return render(request, 'Stromzeiten_app/home.html', context)

def about(request):
    return render(request, 'Stromzeiten_app/about.html', {'title': 'About'})

def chart(request):
    context = {
        'data': Stromzeiten_table.objects.order_by('Date')
    }
    return render(request, 'Stromzeiten_app/chart.html', context)


