from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.


def place_list(request):
    """
    If this is a POST request, the user clicked the Add button on the form.
    Check if the new place is valid, if so, save a new place to the database, 
    and redirect to this same page. This create a GET request to the same route

    If not a POST route, or Place is not valid, display a page with a list of places
    and a form to add a new place
    """
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save()  # create a new place from the form
        if form.is_valid():  # check against DB constraint, are required field present?
            place.save()  # save to the database
            return redirect(
                "place_list"
            )  # redirect to GET view with name place_list i.e. same view

    # If not a POST, or the form is not valid, render the page with the form to
    # add a new place, and list of places

    # places = Place.objects.all() // fetch all in object
    # places = Place.objects.filter(visited=False) //only the visited country
    places = Place.objects.filter(visited=False).order_by("name")
    new_place_form = NewPlaceForm()
    return render(
        request,
        "wishlist/wishlist.html",
        {"places": places, "new_place_form": new_place_form},
    )


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, "wishlist/visited.html", {"visited": visited})


#alternative
def place_was_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = Place.objects.get(pk=pk)
        place.visited = True
        place.save()

    return redirect('place_list')


def place_was_visited(request):
    if request.method == 'POST':
        pk =request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()

    return redirect('place_list')
'''
#alternative for one line filter
def place_was_visited(request):
    if request.method == 'POST':
        place = Place.objects.filter(pk=pk).update(visited=True)

    return redirect('place_list')
'''
