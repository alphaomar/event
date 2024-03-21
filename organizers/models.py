from django.conf import settings
from django.db import models
from users.models import CustomUser
from .managers import OrganizerManger


class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)

    objects = OrganizerManger()

    def __str__(self):
        return f"Organizer: {self.user.username}" if self.user else f"Organizer {self.id}"

    @classmethod
    def create_organizer(cls, user, website="", description="", phone_number="", location=""):
        organizer = cls(user=user, website=website, description=description,
                       phone_number=phone_number, location=location)
        organizer.save()
        return organizer

    def update_organizer(self, website="", description="", phone_number="", location=""):
        self.website = website
        self.description = description
        self.phone_number = phone_number
        self.location = location
        self.save()

    def delete_organizer(self):
        self.delete()

    def is_organizer_active(self):
        return self.user.is_active

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def has_description(self):
        return bool(self.description)

    @property
    def has_phone_number(self):
        """Read-only property to check if the organizer has a phone number."""
        return bool(self.phone_number)

    @property
    def is_local_organizer(self):
        """Read-only property to check if the organizer is based in a local location."""
        local_cities = ["CityA", "CityB", "CityC"]  # Replace with your local cities
        return self.location in local_cities

    @property
    def can_sell_tickets(self):
        """
        Read-only property to check if the organizer is eligible to sell tickets.
        Custom logic based on various conditions such as having a website and being active.
        """
        return self.user.is_active and bool(self.website)

    def save(self, *args, **kwargs):
        # Custom logic before saving, if needed
        self.validate_phone_number()  # Example: Validate phone number format

        # Call the original save method
        super().save(*args, **kwargs)

        # Custom logic after saving, if needed
        self.send_welcome_email()  # Example: Trigger a welcome email to the organizer

    def validate_phone_number(self):
        # Example: Validate that the phone number follows a specific format
        if self.phone_number and not self.phone_number.isdigit():
            raise ValueError("Phone number must contain "
                             ""
                             "only digits.")

    def send_welcome_email(self):
        # Example: Send a welcome email to the organizer
        subject = "Welcome to Our Event Platform"
        message = f"Dear {self.user.first_name},\nThank you for joining our event platform!"
        self.user.email_user(subject, message)

    # Add more custom logic methods as needed...
