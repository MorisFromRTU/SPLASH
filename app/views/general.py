from django.shortcuts import render
from datetime import datetime

def index_page(request):
    context = {}
    return render(request, 'general/index.html', context)

