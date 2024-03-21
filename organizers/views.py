from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Organizer
from events.models import Event
from .forms import OrganizerForm, UpdateOrganizerForm
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.

class OrganizerListView(ListView):
    model = Organizer
    template_name = "organizers/organizerlist.html"
    context_object_name = 'organizers'
    ordering = ['-user__date_joined']
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Organizer.objects.active_organizers().organizers_with_website()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_organizers'] = Organizer.objects.count()
        # context['local_organizers'] = Organizer.objects.organizers_in_city('CityA')
        context['organizers_with_description'] = Organizer.objects.organizers_with_descriptions()
        return context


class OrganizerWithEventListView(ListView):
    model = Event  # Assume there is a ForeignKey or OneToOneField from Event to Organizer
    template_name = 'organizer_event_list.html'
    context_object_name = 'events'
    ordering = ['-date']  # Adjust this based on your Event model
    paginate_by = 10

    def get_queryset(self):
        # Filter events related to the logged-in organizer
        return Event.objects.filter(organizer=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context information if needed
        context['total_events'] = Event.objects.count()  # Total events (all organizers)
        context['organizer'] = self.request.user.id  # Logged-in organizer

        return context


class OrganizerDetailView(DetailView):
    model = Organizer
    template_name = 'organizer_detail.html'
    context_object_name = 'organizers'
    slug_field = "id"
    slug_url_kwarg = "organizer_id"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Organizer.objects.select_related("user").filter(id=self.kwargs["organizer_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.object.event_set.all()
        return context


class OrganizerCreateView(CreateView):
    template_name = "organizers/create.html"
    form_class = OrganizerForm
    extra_context = {"title": "Create organizer"}
    success_url = reverse_lazy("organizer: dashboard")

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrganizerCreateView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class OrganizerUpdateView(UpdateView):
    form_class = UpdateOrganizerForm
    template_name = "organizer/update-profile.html"
    success_url = reverse_lazy("organizer:profile-update")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("Organizer doesn't exist")
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user.organizer
        if obj is None:
            raise Http404("Organizer doesn't exist")
        return obj


class OrganizerDeleteView(DeleteView):
    model = Organizer
    template_name = "organizer/confirm_delete.html"
    success_url = reverse_lazy("organizer:profile-list")  # Adjust the URL name accordingly

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = self.request.user.organizer
        if obj is None:
            raise Http404("Organizer doesn't exist")
        return obj


def home(request):
    return render(request, "base.html")
