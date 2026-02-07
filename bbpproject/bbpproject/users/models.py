from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, BooleanField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import CFPBaseModel


class User(AbstractUser, CFPBaseModel):
    """
    Modèle utilisateur personnalisé.
    Déjà migré → ne pas supprimer de champs existants.
    """

    # Champs déjà présents dans ton code
    name = CharField(_("Nom complet"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None   # type: ignore[assignment]

    # Champs supplémentaires utiles
    email = EmailField(_("email"), unique=True, blank=False, null=False)
    
    # Distinction admin / client
    is_admin = BooleanField(
        _("administrateur"),
        default=False,
        help_text=_("Cochez pour donner les droits staff + superuser")
    )
    
    phone_number = CharField(
        _("numéro de téléphone"),
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )

    loyalty_points = models.PositiveIntegerField(_("points de fidélité"), default=0)
    referral_code = CharField(_("code de parrainage"), max_length=20, blank=True, null=True)
    is_vip = BooleanField(_("client VIP"), default=False)

    # Champs d'audit et statut déjà hérités de CFPBaseModel
    # → created / modified / status

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")

    def __str__(self):
        return self.name or self.username or self.email or str(self.id)

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def is_client(self):
        """Simple utilisateur (non admin)"""
        return not self.is_admin and not self.is_staff and not self.is_superuser

    def save(self, *args, **kwargs):
        # Synchronisation logique : si is_admin → donner is_staff et is_superuser
        if self.is_admin:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)