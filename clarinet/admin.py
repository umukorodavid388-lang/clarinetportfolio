from django.contrib import admin, messages

from .models import BookingRequest, NewsletterSignup


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "engagement_type", "event_date", "venue", "created_at", "is_read")
    list_filter = ("engagement_type", "is_read", "created_at")
    search_fields = ("name", "email", "organisation", "venue", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    actions = ("remove_calendar_dates",)

    @admin.action(description="Remove selected booking dates from the calendar")
    def remove_calendar_dates(self, request, queryset):
        updated = queryset.exclude(event_date__isnull=True).update(event_date=None)
        self.message_user(
            request,
            f"Removed the calendar date from {updated} booking request(s).",
            messages.SUCCESS,
        )


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
