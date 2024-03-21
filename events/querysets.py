# events/querysets.py
from django.db import models
from django.utils import timezone


class EventQuerySet(models.QuerySet):
    def upcoming_events(self):
        """Returns a queryset of upcoming events."""
        return self.filter(date__gt=timezone.now())

    def public_events(self):
        """Returns a queryset of public events."""
        return self.filter(is_private=False)

    # Add more custom querysets as needed...


class TicketQuerySet(models.QuerySet):
    def available_tickets(self):
        """Returns a queryset of available tickets."""
        return self.filter(quantity_available__gt=0)

    # Add more custom querysets as needed...
