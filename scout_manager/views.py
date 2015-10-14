from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def home(request):
    return render_to_response(
        'scout_manager/home.html',
        context_instance=RequestContext(request))


def test(request):
    return render_to_response(
        'scout_manager/test.html',
        context_instance=RequestContext(request))