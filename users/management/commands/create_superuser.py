from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.ru', is_active=True, first_name='Администратор проекта', is_staff=True, is_superuser=True)
        user.set_password('init_init')
        user.save()
