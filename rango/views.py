# Create your views here.

from django.template import RequestContext
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def decode(category_name_url):
    category_name = category_name_url.replace('_', ' ')
    return category_name

def encode(category_name):
    category_url = category_name.replace(' ', '_')
    return category_url

def category(request, category_name_slug):
    # Request our context from the request passed to us.

    
    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # category_name = decode(category_name_url)
     
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    # context_dict = {'category_name': category_name}

    #Django 1.7
    context_dict = {}


    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        context_dict['category_name'] = category.name
        context_dict['category_slug'] = category.slug

        #category = Category.objects.get(name=category_name)
        
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    
    
    return render(request, 'rango/category.html', context_dict)



def index(request):
    
    # Request the Context of the request
    # The context contains information such as the client's machine details, for example.

    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    #Lesson 4
    #context_dict = {'boldmessage' : "I am bold font from the context."}
    
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    try:
        toppages = Page.objects.order_by('-view')[:5]
        
        context_dict['toppages'] = toppages
        
    except Page.DoesNotExist:
        pass
    
    #The following two lines are new.
    #We loop through each category returned, and create a URL attribute.
    #This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = encode(category.name)
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    #Lesson 4
    return render(request, 'rango/index.html', context_dict)
    
    #Lesson 3
    #return HttpResponse("Rango says hello world! <a href='/rango/about/'>About</a>")

#Lesson 3 Excercise
def about(request):
    context = RequestContext(request)
    
    context_dict = {'aboutmessage': "see that everything is ok"}

    return render(request, 'rango/about.html', context_dict)
    
    #return HttpResponse("Rango says: here is the about page. <a href='/rango/'>Index</a>")

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #Save the new form to the database
            cat = form.save(commit=True)
            print cat, cat.slug
            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form':form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'category_slug': cat.slug}

    return render(request, 'rango/add_page.html', context_dict)
