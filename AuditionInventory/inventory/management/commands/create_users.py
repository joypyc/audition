from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_model = get_user_model()
        guest, created = user_model.objects.get_or_create(
            username='guest'
        )
        guest.set_password('guest')
        guest.save()

        admin_user, created = user_model.objects.get_or_create(
            username='manager'
        )
        admin_user.set_password('manager')
        admin_user.save()