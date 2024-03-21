# events/managers.py
from django.db import models
from .querysets import EventQuerySet, TicketQuerySet


class EventManager(models.Manager):
    def get_queryset(self):
        """Returns the custom queryset for the Event model."""
        return EventQuerySet(self.model, using=self._db)

    def upcoming_events(self):
        """Returns a queryset of upcoming events."""
        return self.get_queryset().upcoming_events()

    def public_events(self):
        """Returns a queryset of public events."""
        return self.get_queryset().public_events()

    # Add more custom manager methods as needed...


class TicketManager(models.Manager):
    def get_queryset(self):
        """Returns the custom queryset for the Ticket model."""
        return TicketQuerySet(self.model, using=self._db)

    def available_tickets(self):
        """Returns a queryset of available tickets."""
        return self.get_queryset().available_tickets()

    # Add more custom manager methods as needed...
