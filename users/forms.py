from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class OrganizerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    organization_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(OrganizerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["organization_name"].label = "Organization Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["organization_name"].widget.attrs.update({"placeholder": "Enter Organization Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "organization_name", "email", "password1", "password2"]
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
            "organization_name": {"required": "Organization name is required"},
        }

    def save(self, commit=True):
        user = super(OrganizerRegistrationForm, self).save(commit=False)
        user.role = "organizer"
        if commit:
            user.save()
        return user


class AttendeeRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AttendeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
        }

    def save(self, commit=True):
        user = super(AttendeeRegistrationForm, self).save(commit=False)
        user.role = "attendee"
        if commit:
            user.save()
        return user



class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
        }

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.role = "user"
        if commit:
            user.save()
        return user