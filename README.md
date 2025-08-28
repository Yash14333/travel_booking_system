# Travel Booking Project (Ready-to-run)

## Quickstart (Windows)
1. `cd travel_booking_project`
2. `python -m venv env`
3. `env\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`  # this will auto-seed demo users and sample travel options
6. `python manage.py runserver`
7. Open http://127.0.0.1:8000/

## Default accounts (auto-created on migrate)
- admin / admin123  (superuser)
- testuser / testpass123  (regular user)

## Files included
- manage.py (root), requirements.txt, README.md
- travel_booking/ (Django settings)
- bookings/ (app with models, views, templates, static, tests)
- Dockerfile + docker-compose.yml (optional)
