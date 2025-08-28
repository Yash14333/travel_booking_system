from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        # connect post_migrate signal to seed function
        from . import seed
        post_migrate.connect(seed.create_demo_data, sender=self)
