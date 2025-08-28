def create_demo_data(sender, **kwargs):
    try:
        from django.contrib.auth.models import User
        from .models import TravelOption
        from django.utils import timezone
        from datetime import timedelta
        from decimal import Decimal
        import random
        # create admin if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        # create testuser
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        # seed travel options only if none exist
        if TravelOption.objects.count() == 0:
            now = timezone.now()
            samples = [
                ('FLIGHT','DEL','BOM', 1, Decimal('3500.00')),
                ('TRAIN','NDLS','BCT', 2, Decimal('750.00')),
                ('BUS','PUNE','MUM', 3, Decimal('300.00')),
                ('FLIGHT','BLR','DEL', 5, Decimal('4200.00')),
                ('TRAIN','MAS','CBE', 4, Decimal('500.00')),
            ]
            for i, (t, src, dst, days, price) in enumerate(samples, start=1):
                TravelOption.objects.create(
                    travel_id=f"SAMPLE{i:03}",
                    type=t,
                    source=src,
                    destination=dst,
                    departure_datetime=now + timedelta(days=days, hours=random.randint(1,12)),
                    price=price,
                    available_seats=random.randint(20,120)
                )
    except Exception as e:
        # during initial migrations, models may not be ready; ignore failures silently
        print('seed error:', e)
