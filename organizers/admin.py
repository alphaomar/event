from django.contrib import admin
from .models import Organizer


# Register your models here.

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass
