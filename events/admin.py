# events/admin.py
from django.contrib import admin
from .models import Event, EventCategory, Tag, Ticket, TicketType, Order

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(Tag)
admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(Order)
