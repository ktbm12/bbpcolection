import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, to_email, template_name, context):
    """
    Celery task to send emails in the background.
    """
    try:
        # Add common context
        context['year'] = datetime.now().year
        context['site_name'] = 'bbpcollection'
        
        # Render HTML content
        html_content = render_to_string(template_name, context)
        # Create text version by stripping tags
        text_content = strip_tags(html_content)
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@bbpcollection.com',
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Send
        msg.send()
        logger.info(f"Email sent successfully to {to_email} with subject: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_templated_email(subject, to_email, template_name, context):
    """
    Helper function to enqueue an email sending task.
    """
    send_email_task.delay(subject, to_email, template_name, context)
