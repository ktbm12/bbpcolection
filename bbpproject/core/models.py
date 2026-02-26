# core/models.py
from uuid import uuid4

from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class CFPBaseModel(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name="Identifier",
        help_text="Universal unique identifier"
    )

    is_active = models.BooleanField(
        _("active / visible"),
        default=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        return f"{self.__class__.__name__} ({self.id})"


class LegalPage(CFPBaseModel):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), unique=True, max_length=255)
    content = models.TextField(_("content"), help_text=_("Content in HTML or raw text format"))

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("legal page")
        verbose_name_plural = _("legal pages")

    def __str__(self):
        return self.title


class PrivacyPolicy(CFPBaseModel):
    """
    Singleton model for Privacy Policy with US-compliant default English text.
    """
    title = models.CharField(_("title"), max_length=200, default="Privacy Policy")
    content = models.TextField(_("content"), default="""
# Privacy Policy
Last Updated: February 26, 2026

At BBP Collection, we are committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your personal information when you visit our website or make a purchase.

## 1. Information We Collect
We collect information you provide directly to us, such as your name, email address, shipping address, and payment information (processed securely through Stripe). We also collect automated data about your device and browsing activity via cookies.

## 2. How We Use Your Information
We use your data to:
- Process and fulfill your orders.
- Communicate with you about your purchases and promotional offers.
- Improve our website and customer experience.
- Comply with legal obligations and prevent fraud.

## 3. Data Protection
We implement industry-standard security measures to protect your personal data. However, no method of transmission over the Internet is 100% secure.

## 4. Third-Party Services
We share information with third-party providers only as necessary to provide our services, such as Stripe for payment processing and shipping carriers. These providers have their own privacy policies.

## 5. Your Rights (CCPA/GDPR)
Depending on your residency, you may have rights to access, update, or delete your personal information. Contact us at the email below for requests.

## 6. Children's Privacy
Our website is not intended for children under 13. We do not knowingly collect data from children (COPPA Compliance).

## 7. Changes to This Policy
We may update this policy from time to time. Changes will be posted on this page with an updated date.

## 8. Contact Us
If you have questions about this Privacy Policy, please contact us at:
Email: support@bbpcollection.com
""")

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("privacy policy")
        verbose_name_plural = _("privacy policy")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self._state.adding and PrivacyPolicy.objects.exists():
            from django.core.exceptions import ValidationError
            raise ValidationError(_("There can be only one Privacy Policy instance."))
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Use a fixed UUID for the singleton Privacy Policy
        singleton_id = "00000000-0000-0000-0000-000000000001"
        obj, created = cls.objects.get_or_create(id=singleton_id)
        return obj