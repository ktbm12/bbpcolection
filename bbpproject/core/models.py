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
        verbose_name="Identifiant",
        help_text="Identifiant unique universel"
    )

    is_active = models.BooleanField(
        _("actif / visible"),
        default=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        return f"{self.__class__.__name__} ({self.id})"


class LegalPage(CFPBaseModel):
    title = models.CharField(_("titre"), max_length=200)
    slug = models.SlugField(_("slug"), unique=True, max_length=255)
    content = models.TextField(_("contenu"), help_text=_("Contenu au format HTML ou texte brut"))

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("page légale")
        verbose_name_plural = _("pages légales")

    def __str__(self):
        return self.title