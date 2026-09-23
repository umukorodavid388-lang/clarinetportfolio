from django import forms

from .models import BookingRequest, NewsletterSignup


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = (
            "name",
            "email",
            "organisation",
            "engagement_type",
            "event_date",
            "venue",
            "message",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "organisation": forms.TextInput(attrs={"class": "form-control", "placeholder": "Orchestra, venue, school…"}),
            "engagement_type": forms.Select(attrs={"class": "form-select"}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "venue": forms.TextInput(attrs={"class": "form-control", "placeholder": "City or venue"}),
            "message": forms.Textarea(attrs={"rows": 5, "class": "form-control", "placeholder": "Tell me about the engagement…"}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please add a little more detail (10 characters minimum).")
        return message


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ("email",)
