from django.db import models


class BookingRequest(models.Model):
    """An enquiry sent from the booking / contact form."""

    ENGAGEMENT_CHOICES = [
        ("recital", "Solo recital"),
        ("concerto", "Concerto / orchestral soloist"),
        ("chamber", "Chamber music"),
        ("session", "Studio / session recording"),
        ("orchestra", "Orchestra / orchestral clarinetist"),
        ("masterclass", "Masterclass / teaching"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    organisation = models.CharField(max_length=160, blank=True)
    engagement_type = models.CharField(max_length=32, choices=ENGAGEMENT_CHOICES, default="recital")
    event_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "booking request"

    def __str__(self):
        return f"{self.name} — {self.get_engagement_type_display()}"


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
