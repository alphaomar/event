from django import forms
from .models import Organizer
from datetime import datetime


class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['website', 'description', 'phone_number', 'location']
        labels = {
            'website': 'Website',
            'description': 'Description',
            'phone_number': 'Phone Number',
            'location': 'Location',
        }
        widgets = {
            'description': forms.Textarea(attrs={'row': 4}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number '}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError('phone number must be digits')
        return phone_number

    def clean_location(self):
        location = self.cleaned_data['location']
        return location

    def is_valid(self):
        valid = super(OrganizerForm, self).is_valid()
        if not valid:
            return False
        website = self.cleaned_data.get('website')
        if not website or not website.startswith('http'):
            self.add_error('website', 'Please enter a valid website starting with http')
        return valid

    def save(self, commit=True):
        organizer = super(OrganizerForm, self).save(commit=False)
        if commit:
            organizer.save()
        return organizer


class UpdateOrganizerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateOrganizerForm, self).__init__(*args, **kwargs)
        self.fields["website"].widget.attrs.update({"placeholder": "Enter Website"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter Description"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "Enter Phone Number"})
        self.fields["location"].widget.attrs.update({"placeholder": "Enter Location"})

    class Meta:
        model = Organizer
        fields = ["website", "description", "phone_number", "location"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Add custom validation for phone numbers if needed
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_number

    def save(self, commit=True):
        organizer = super(UpdateOrganizerForm, self).save(commit=False)
        if commit:
            organizer.save()
        return organizer
