from django.core.management.base import BaseCommand
from core.models import LegalPage
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Initialize default legal pages'

    def handle(self, *args, **options):
        pages = [
            {
                'title': 'Terms of Use',
                'slug': 'terms-of-use',
                'content': """
<h2>1. Acceptance of Terms</h2>
<p>By accessing and using bbpcollection.com, you accept and agree to be bound by the terms and provision of this agreement.</p>

<h2>2. Use of the Site</h2>
<p>You may use our site for personal, non-commercial purposes. You must not use this site for any illegal or unauthorized purpose.</p>

<h2>3. Intellectual Property</h2>
<p>All content on this site, including hair style imagery, text, and logos, is the property of BBP Collection and protected by copyright laws.</p>

<h2>4. Limitation of Liability</h2>
<p>BBP Collection shall not be liable for any direct, indirect, incidental, or consequential damages resulting from the use or inability to use our services.</p>

<h2>5. Governing Law</h2>
<p>These terms shall be governed by and construed in accordance with the laws of the United States.</p>
"""
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'content': """
<h2>1. Information We Collect</h2>
<p>We collect information you provide directly to us, such as your name, email address, shipping address, and payment information (processed securely through Stripe).</p>

<h2>2. How We Use Your Information</h2>
<p>We use your data to process orders, communicate with you, and improve our services. We do not sell your personal information to third parties.</p>

<h2>3. Data Security</h2>
<p>We implement industry-standard security measures to protect your personal data. However, no method of transmission over the Internet is 100% secure.</p>

<h2>4. Cookies</h2>
<p>We use cookies to enhance your browsing experience and analyze site traffic.</p>

<h2>5. Your Rights</h2>
<p>Depending on your location, you may have the right to access, update, or delete your personal information.</p>

<h2>6. Contact Us</h2>
<p>For any questions regarding this policy, contact us at support@bbpcollection.com.</p>
"""
            }
        ]

        for page_data in pages:
            obj, created = LegalPage.objects.update_or_create(
                slug=page_data['slug'],
                defaults={
                    'title': page_data['title'],
                    'content': page_data['content'],
                    'is_active': True
                }
            )
            status = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f'Page "{page_data["title"]}" {status}.'))
