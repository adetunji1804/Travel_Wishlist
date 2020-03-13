from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


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

    
    #display non visited countries, use name column to order the list
    new_place_form = NewPlaceForm()
    places = Place.objects.filter(visited=False).order_by("name") 
    return render(
        request,
        "wishlist/wishlist.html",
        {"places": places, "new_place_form": new_place_form},
    )


def places_visited(request):
    visited = Place.objects.filter(visited=True) #display visited countries
    return render(request, "wishlist/visited.html", {"visited": visited})


# handling a post request with PK not in database
def place_was_visited(request):
    if request.method == 'POST':
        pk =request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()

    return redirect('place_list')
