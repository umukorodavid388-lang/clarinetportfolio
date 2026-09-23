# Clarinet Performance Portfolio

A Django-powered performance portfolio for a clarinettist, with an HTML / CSS / Bootstrap 5 / JavaScript front end.

## What's inside

- Pages: Home, Biography, Performances, Listen (media), Services, Service detail, Booking & Contact
- Light/dark theme toggle (saved in the browser)
- Scroll-reveal animations, responsive Bootstrap layout
- Booking request form (AJAX) saved to the database + email notification
- Newsletter signup (AJAX)
- Django admin for booking requests and newsletter signups

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations clarinet
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000

## Editing your content

All text content (name, biography, performances, recordings, services, press quotes,
training, social links, statistics) lives in **`clarinet/data.py`**. Edit that one file
and every page updates.

## Images and press kit

- Replace `static/img/hero-portrait.jpg` and `static/img/stage.jpg` with real photos.
- Replace `static/files/press-kit.pdf` with your real press kit / EPK.

## Email notifications

By default emails print to the terminal (console backend). For real email, edit
`config/settings.py`:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "you@example.com"
EMAIL_HOST_PASSWORD = "your-app-password"
DEFAULT_FROM_EMAIL = "you@example.com"
NOTIFY_EMAIL = "you@example.com"
```

## Deployment notes

- Set `DEBUG = False`, a real `SECRET_KEY`, and your domain in `ALLOWED_HOSTS`.
- Run `python manage.py collectstatic` and serve `staticfiles/` (e.g. WhiteNoise or Nginx).
