from django import forms
from .models import Event, Ticket
from datetime import datetime


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'organizer', 'date', 'location', 'category',
                  'tags', 'image', 'is_private', 'category_type']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'organizer': 'Organizer',
            'date': 'Date',
            'location': 'Location',
            'category': 'Category',
            'tags': 'Tags',
            'image': 'Image',
            'is_private': 'Is Private',
            'category_type': 'Category Type',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']

        if date < datetime.now().date():
            raise forms.ValidationError('Event must be in the future.')
        return date

    def clean_location(self):
        location = self.cleaned_data['location']
        return location

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 6:
            raise forms.ValidationError("You can add more than six 6 tags")
        return tags

    def is_valid(self):
        valid = super(EventForm, self).is_valid()

        if not valid:
            return False

        if self.cleaned_data.get('is_private') and not self.cleaned_data.get('category'):
            self.add_error('category', 'Private events must have a category.')
        return valid

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)

        if commit:
            event.save()
            for tag in self.cleaned_data['tags']:
                event.tags.add(tag)
        return event


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'name', 'price', 'quantity_available', 'ticket_type']
        labels = {
            'event': 'Event',
            'name': 'Name',
            'price': 'Price',
            'quantity_available': 'Quantity Available',
            'ticket_type': 'Ticket Type',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero')
        return price

    def clean_quantity_available(self):
        quantity_available = self.cleaned_data['quantity_available']
        if quantity_available <= 0:
            raise forms.ValidationError('Quantity available nust be greater than zero.')
        return quantity_available

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def is_valid(self):
        valid = super(TicketForm, self).is_valid()

        # Add custom conditions for validity
        if not valid:
            return False

        # Additional custom validation logic
        if self.cleaned_data.get('price') and self.cleaned_data.get('quantity_available'):
            if self.cleaned_data['quantity_available'] > 10 and self.cleaned_data['price'] > 100:
                self.add_error(None, 'Discounts available for quantities over 10 and prices over 100.')

        return valid

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        if commit:
            ticket.save()
        return ticket
