from django.shortcuts import render

def index(request):
    context = {
        'title': 'G-Shop',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'G-Shop | About us',
    }
    return render(request, 'main/about.html', context)