from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response

# Create your views here.

def test(request):
    return render_to_response(
        'scout_manager/test.html',
        context_instance=RequestContext(request))
        
def app(request):
    return render_to_response(
        'scout_manager/app.html',
        context_instance=RequestContext(request))


def add(request):
    return render_to_response(
        'scout_manager/add.html',
        context_instance=RequestContext(request))
        
def item(request):
    return render_to_response(
        'scout_manager/item.html',
        context_instance=RequestContext(request))


def publish(request):
    return render_to_response(
        'scout_manager/publish.html',
        context_instance=RequestContext(request))
        
def space(request):
    return render_to_response(
        'scout_manager/space.html',
        context_instance=RequestContext(request))
