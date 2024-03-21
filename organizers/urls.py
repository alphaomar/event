# urls.py
from django.urls import path
from .views import OrganizerWithEventListView, OrganizerListView, home

urlpatterns = [
    path('', OrganizerListView.as_view(), name='organizer_list'),
    path('organizer-events/', OrganizerWithEventListView.as_view(), name='organizer_event_list'),
    path("home/", home, name="home")
    # Add other URL patterns as needed
]
