from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

def index(request):
    return render(request, 'home/index.html')

def privacy(request):
    return render(request, 'home/privacy.html')