from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("performances/", views.performances, name="performances"),
    path("calendar/", views.booking_calendar, name="calendar"),
    path("calendar/<int:booking_id>/remove-date/", views.remove_calendar_booking_date, name="remove_calendar_booking_date"),
    path("media/", views.media, name="media"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.contact_success, name="contact_success"),
    path("newsletter/", views.newsletter, name="newsletter"),
]
