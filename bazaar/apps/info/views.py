from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import RequestContext, loader

def index(request):
    template = loader.get_template('info/index.html')

    return render(request, 'info/index.html')


def disclaimer(request):

    template = loader.get_template('info/disclaimer.html')

    return render(request, 'info/disclaimer.html')