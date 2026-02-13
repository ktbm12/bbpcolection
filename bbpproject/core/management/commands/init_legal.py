from django.core.management.base import BaseCommand
from core.models import LegalPage
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Initialise les pages légales par défaut'

    def handle(self, *args, **options):
        pages = [
            {
                'title': 'Terms of Use',
                'content': '<h2>Conditions d\'utilisation</h2><p>Bienvenue sur bbpcollection. En utilisant ce site, vous acceptez nos conditions...</p>'
            },
            {
                'title': 'Privacy Policy',
                'content': '<h2>Politique de confidentialité</h2><p>Nous accordons une grande importance à la protection de vos données personnelles...</p>'
            }
        ]

        for page_data in pages:
            slug = slugify(page_data['title'])
            obj, created = LegalPage.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': page_data['title'],
                    'content': page_data['content'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Page "{page_data["title"]}" créée.'))
            else:
                self.stdout.write(self.style.WARNING(f'Page "{page_data["title"]}" existe déjà.'))
