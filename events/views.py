from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from .forms import EventForm, TicketForm
from .models import Event, Ticket

# Create your views here.


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_events'] = Event.objects.all()
        return context



