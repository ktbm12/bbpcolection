from django.core.management.base import BaseCommand
from core.models import LegalPage
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Initialize default legal pages'

    def handle(self, *args, **options):
        pages = [
            {
                'title': 'Terms of Use',
                'content': '<h2>Terms of Use</h2><p>Welcome to bbpcollection. By using this site, you agree to our terms...</p>'
            },
            {
                'title': 'Privacy Policy',
                'content': '<h2>Privacy Policy</h2><p>We value the protection of your personal data...</p>'
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
                self.stdout.write(self.style.SUCCESS(f'Page "{page_data["title"]}" created.'))
            else:
                # Update content if already exists to ensure English
                obj.title = page_data['title']
                obj.content = page_data['content']
                obj.save()
                self.stdout.write(self.style.SUCCESS(f'Page "{page_data["title"]}" updated to English.'))
