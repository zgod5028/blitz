from django.shortcuts import render

def index(request):
    return render(request, 'mine/index.html')
