from django.contrib import admin

from .models import BookingRequest, NewsletterSignup


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "engagement_type", "event_date", "venue", "created_at", "is_read")
    list_filter = ("engagement_type", "is_read", "created_at")
    search_fields = ("name", "email", "organisation", "venue", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
