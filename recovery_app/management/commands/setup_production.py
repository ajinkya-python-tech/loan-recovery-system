from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):

    help = 'Setup production admin'

    def handle(self, *args, **kwargs):

        User = get_user_model()

        # DELETE ALL EXISTING USERS
        #User.objects.all().delete()

        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Create admin only if no superuser exists
        if not User.objects.filter(is_superuser=True).exists():

            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )

            self.stdout.write(
                self.style.SUCCESS('Superuser created successfully')
            )

        else:

            self.stdout.write('Superuser already exists')