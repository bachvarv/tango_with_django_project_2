# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    
    # Request the Context of the request
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage' : "I am bold font from the context."}
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    #Lesson 4
    return render_to_response('rango\index.html', context_dict, context)
    
    #Lesson 3
    #return HttpResponse("Rango says hello world! <a href='/rango/about/'>About</a>")

#Lesson 3 Excercise
def about(request):
    context = RequestContext(request)
    
    context_dict = {'aboutmessage': "see that everything is ok"}
    
    return render_to_response('rango\\about.html', context_dict, context)
    
    #return HttpResponse("Rango says: here is the about page. <a href='/rango/'>Index</a>")