from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from core.email_utils import send_templated_email

@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    """
    Send a welcome email to the user after they sign up.
    """
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    
    context = {
        'user': user,
        'shop_url': f"{protocol}://{domain}{reverse('product:product_list')}"
    }
    
    send_templated_email(
        subject="Bienvenue chez bbpcollection ! ✨",
        to_email=user.email,
        template_name='emails/welcome_email.html',
        context=context
    )
