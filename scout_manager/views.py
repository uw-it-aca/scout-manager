from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from htmlmin.decorators import minified_response

# Create your views here.

def home(request):
    return render_to_response(
        'scout_manager/home.html',
        context_instance=RequestContext(request))


def test(request):
    return render_to_response(
        'scout_manager/test.html',
        context_instance=RequestContext(request))