from django.db import models
from .queryset import OrganizerQuerySet


class OrganizerManger(models.Manager):
    def get_queryset(self):
        return OrganizerQuerySet(self.model, using=self._db)

    def active_organizers(self):
        return self.get_queryset().filter(user__is_active=True)

    def organizers_with_website(self):
        return self.get_queryset().organizers_with_website()

    def organizers_with_descriptions(self):
        return self.get_queryset().organizers_with_descriptions()

    def organizers_in_city(self, city):
        return self.get_queryset().organizers_in_city(city)

    def search_organizers(self, query):
        return self.get_queryset().search_organizers(query)
