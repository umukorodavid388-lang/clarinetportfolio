from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from . import data
from .forms import BookingForm, NewsletterForm

from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def home(request):
    upcoming = [p for p in data.PERFORMANCES if p["status"] == "upcoming"]
    return render(request, "clarinet/index.html", {
        "active": "home",
        "highlights": data.HIGHLIGHTS,
        "upcoming": upcoming[:3],
        "services": data.SERVICES[:6],
        "recordings": data.RECORDINGS[:3],
    })


def about(request):
    return render(request, "clarinet/about.html", {
        "active": "about",
        "training": data.TRAINING,
        "repertoire": data.REPERTOIRE,
        # "press": data.PRESS,
    })


def performances(request):
    return render(request, "clarinet/performances.html", {
        "active": "performances",
        "upcoming": [p for p in data.PERFORMANCES if p["status"] == "upcoming"],
        "past": [p for p in data.PERFORMANCES if p["status"] == "past"],
    })


def media(request):
    return render(request, "clarinet/media.html", {
        "active": "media",
        "recordings": data.RECORDINGS,
    })


def services(request):
    return render(request, "clarinet/services.html", {
        "active": "services",
        "services": data.SERVICES,
    })


def service_detail(request, slug):
    service = data.get_service(slug)
    if service is None:
        raise Http404("Service not found")
    others = [s for s in data.SERVICES if s["slug"] != slug][:3]
    return render(request, "clarinet/service_detail.html", {
        "active": "services",
        "service": service,
        "others": others,
    })


def contact(request):
    artist = data.ARTIST
    channels = [
        {"label": "Email", "value": artist["email"], "href": "mailto:" + artist["email"]},
        {"label": "Phone", "value": artist["phone"], "href": "tel:" + artist["phone"].replace(" ", "")},
        {"label": "Based in", "value": artist["location"]},
    ]

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            _notify_owner(booking)
            if _is_ajax(request):
                return JsonResponse({
                    "success": True,
                    "message": "Thank you — your enquiry is in. I usually reply within two days.",
                })
            return redirect("contact_success")
        if _is_ajax(request):
            return JsonResponse(
                {"success": False, "errors": form.errors, "message": "Please check the highlighted fields."},
                status=400,
            )
    else:
        form = BookingForm()

    return render(request, "clarinet/contact.html", {
        "active": "contact",
        "form": form,
        "channels": channels,
    })


def contact_success(request):
    return render(request, "clarinet/contact.html", {
        "active": "contact",
        "form": BookingForm(),
        "channels": [],
        "sent": True,
    })


def newsletter(request):
    if request.method != "POST":
        raise Http404
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "message": "You're on the list — thank you."})
    return JsonResponse(
        {"success": False, "message": "That email is already subscribed or invalid."},
        status=400,
    )


def _notify_owner(booking):
    """Email the artist whenever a new booking enquiry arrives."""
    recipient = settings.NOTIFY_EMAIL
    if not recipient:
        return

    engagement = booking.get_engagement_type_display()
    subject = f"[Booking] {booking.name} — {engagement}"

    # Plain-text fallback (for clients that block HTML)
    text_body = (
        "New booking enquiry\n\n"
        f"Name:         {booking.name}\n"
        f"Email:        {booking.email}\n"
        f"Organisation: {booking.organisation or '—'}\n"
        f"Engagement:   {engagement}\n"
        f"Date:         {booking.event_date.strftime('%d %B %Y') if booking.event_date else 'not specified'}\n"
        f"Venue:        {booking.venue or '—'}\n"
        f"Received:     {booking.created_at:%d %B %Y, %H:%M}\n\n"
        f"{booking.message}\n"
    )

    def row(label, value):
        return f"""
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;color:#888;font-size:13px;
                     font-family:Georgia,serif;width:120px;vertical-align:top;">{label}</td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;color:#222;font-size:14px;
                     font-family:Georgia,serif;vertical-align:top;">{escape(value)}</td>
        </tr>"""

    rows = "".join([
        row("Name", booking.name),
        row("Email", booking.email),
        row("Organisation", booking.organisation or "—"),
        row("Engagement", engagement),
        row("Date", booking.event_date.strftime("%d %B %Y").lstrip("0") if booking.event_date else "Not specified"),
        row("Venue", booking.venue or "—"),
        row("Received", f"{booking.created_at:%d %B %Y, %H:%M}"),
    ])

    html_body = f"""
    <div style="background:#f4f2ee;padding:32px 16px;font-family:Georgia,serif;">
      <table role="presentation" width="100%" style="max-width:560px;margin:0 auto;
             background:#ffffff;border-radius:4px;overflow:hidden;
             border:1px solid #e6e2da;">
        <tr>
          <td style="background:#1f2a24;padding:24px 32px;">
            <p style="margin:0;color:#e9e4d8;font-size:12px;letter-spacing:2px;
                      text-transform:uppercase;font-family:Georgia,serif;">New Enquiry</p>
            <h1 style="margin:6px 0 0;color:#ffffff;font-size:20px;font-weight:normal;
                       font-family:Georgia,serif;">{escape(booking.name)}</h1>
          </td>
        </tr>
        <tr>
          <td style="padding:28px 32px 8px;">
            <table role="presentation" width="100%" style="border-collapse:collapse;">
              {rows}
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:20px 32px 28px;">
            <p style="margin:0 0 6px;color:#888;font-size:12px;letter-spacing:1px;
                      text-transform:uppercase;font-family:Georgia,serif;">Message</p>
            <p style="margin:0;color:#333;font-size:14px;line-height:1.6;
                      font-family:Georgia,serif;white-space:pre-wrap;">{escape(booking.message)}</p>
          </td>
        </tr>
        <tr>
          <td style="background:#f4f2ee;padding:16px 32px;text-align:center;">
            <p style="margin:0;color:#999;font-size:12px;font-family:Georgia,serif;">
              Reply directly to this email to respond to {escape(booking.name)}.
            </p>
          </td>
        </tr>
      </table>
    </div>
    """

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[booking.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()