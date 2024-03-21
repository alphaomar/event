# events/models.py

from django.db import models
from django.contrib.auth import get_user_model
from organizers.models import Organizer
from users.models import CustomUser
from .managers import EventManager, TicketManager

User = get_user_model()


class DateTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TicketType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(DateTracking):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    is_private = models.BooleanField(default=False)

    objects = EventManager()

    EVENT_CHOICES = [
        ('concert', 'Concert'),
        ('conference', 'Conference'),
        ('exhibition', 'Exhibition'),
        # Add more choices as needed
    ]

    category_type = models.CharField(max_length=20, choices=EVENT_CHOICES)

    def __str__(self):
        return self.title

    @property
    def is_event_upcoming(self):
        """Read-only property to check if the event is upcoming."""
        from django.utils import timezone
        return self.date > timezone.now()

    @classmethod
    def create_event(cls, title, description, organizer, date, location, category_type, is_private=False):
        """Class method to create and save a new event."""
        event = cls(
            title=title,
            description=description,
            organizer=organizer,
            date=date,
            location=location,
            category_type=category_type,
            is_private=is_private
        )
        event.save()
        return event

    def update_event(self, title=None, description=None, date=None, location=None, category_type=None, is_private=None):
        """Model method to update the event attributes."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if date is not None:
            self.date = date
        if location is not None:
            self.location = location
        if category_type is not None:
            self.category_type = category_type
        if is_private is not None:
            self.is_private = is_private
        self.save()

    def delete_event(self):
        """Model method to delete the event."""
        self.delete()

    # Add more custom logic or methods as needed...


class Ticket(DateTracking):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    ticket_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)

    objects = TicketManager()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    @property
    def is_ticket_available(self):
        """Read-only property to check if the ticket is available."""
        return self.quantity_available > 0

    def decrease_quantity(self, quantity=1):
        """Model method to decrease the available quantity of the ticket."""
        if self.quantity_available >= quantity:
            self.quantity_available -= quantity
            self.save()

    # Add more custom logic or methods as needed...


class Order(DateTracking):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_info = models.TextField(null=True, blank=True)
    confirmation_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Organizer: {self.user.username}" if self.user else f"Organizer {self.id} - {self.ticket.name}"
