from django.shortcuts import render

def index(request):
    return render(request, 'taller_1/taller_1.html')
