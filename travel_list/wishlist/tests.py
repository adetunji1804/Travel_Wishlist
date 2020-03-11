from django.test import TestCase
from django.urls import reverse

from .models import Place

# tests here.
class TestHomePageIsEmptyList(TestCase):
    def test_load_home_page_shows_empty_list(self):
        response = self.client.get(reverse("place_list"))
        self.assertTemplateUsed(response, "wishlist/wishlist.html")
        self.assertFalse(response.context["places"])
        self.assertContains(response, "You have no places in your wishlist")


class TestWishList(TestCase):
    fixtures = ["test_places"]

    def test_view_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse("place_list"))
        self.assertTemplateUsed(response, "wishlist/wishlist.html")

        self.assertContains(response, "Tokyo")
        self.assertContains(response, "New York")
        self.assertNotContains(response, "San Francisco")
        self.assertNotContains(response, "Moab")


class TestNoPlaceVisited(TestCase):
    def test_no_place_visited(self):

        response = self.client.get(reverse("places_visited"))
        self.assertTemplateUsed(response, "wishlist/visited.html")
        self.assertFalse(response.context["visited"])
        self.assertContains(response, "You have not visited any place yet")


class TestVisitedPlaces(TestCase):
    fixtures = ["test_places"]

    def test_contains_visited_places(self):
        response = self.client.get(reverse("places_visited"))
        self.assertTemplateUsed(response, "wishlist/visited.html")

        self.assertContains(response, "San Francisco")
        self.assertContains(response, "Moab")
        self.assertNotContains(response, "New York")
        self.assertNotContains(response, "Tokyo")

class TestAddNewPlace(TestCase):
    def test_add_new_unvisited_place_to_wishlist(self):
        response= self.client.post(reverse('place_list'), {'name':'Tokyo', 'visited':False}, follow=True)

        #check correct template was used
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')

        #what data was used to populate the template?
        response_places = response.context['places']
        # should be 1 item
        self.assertEqual(len(response_places), 1)
        tokyo_response = response_places[0]

        #expect this data to be in the database. Use get() to get data with
        #the valus expected. will throw an exception if no data, or more than one row,
        #matches. Remeber throwing an exception will cause this test to fail
        tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

        #is the data used to render the template, the same as the data in the database?
        self.assertEqual(tokyo_response, tokyo_in_database)