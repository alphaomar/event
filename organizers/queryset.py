from django.db import models
from users.models import CustomUser


class OrganizerQuerySet(models.QuerySet):
    def organizers_with_website(self):
        return self.filter(website__isnull=False)

    def organizers_with_descriptions(self):
        return self.exclude(description="")

    def organizers_in_city(self, city):
        return self.filter(location__iscontains=city)

    def search_organizers(self, query):
        return self.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query) |
            models.Q(location__icontains=query)
        )