from django.shortcuts import render, render_to_response
from django.views import generic
from .forms import SelectionForm
import re


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "viz/index.html"


# view that either renders the list of possible data for graphs, or list of graphs that are applicable to be
# drawn for the data given
def selection(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SelectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # redirect to a new URL: Should be the suggestion.html(list of graphs that are applicable
            # to be plotted) template
            return render_to_response('viz/suggestion.html', {"fields": form.cleaned_data['fields']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SelectionForm()

    return render(request, 'viz/selection.html', {'form': form})


def bar(request, fields):
    # fields = request.GET.get('page')
    field_string = re.sub('[\[\]\']', '', fields)
    columns = field_string.split(", ")

    return render_to_response('viz/bar.html')
