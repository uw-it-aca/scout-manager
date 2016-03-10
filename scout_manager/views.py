from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response

# Create your views here.

def list(request):
    return render_to_response(
        'scout_manager/list.html',
        context_instance=RequestContext(request))


def add(request):
    return render_to_response(
        'scout_manager/add.html',
        context_instance=RequestContext(request))
        
def item(request):
    return render_to_response(
        'scout_manager/item.html',
        context_instance=RequestContext(request))


def future(request):
    return render_to_response(
        'scout_manager/future.html',
        context_instance=RequestContext(request))
        
def space(request):
    return render_to_response(
        'scout_manager/space.html',
        context_instance=RequestContext(request))
