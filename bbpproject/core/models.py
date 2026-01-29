from django.db import models

# Create your models here.
# core/models.py  ou  common/models.py

from django.db import models
from model_utils.models import TimeStampedModel, ActivatorModel
from uuid import uuid4


class CFPBaseModel(TimeStampedModel, ActivatorModel):
    """
    Modèle de base CFP simplifié avec UUID, timestamps et activation.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name="Identifiant",
        help_text="Identifiant unique universel"
    )

    class Meta:
        abstract = True
        ordering = ['-created']     # tri par date de création descendante

    def __str__(self):
        return f"{self.__class__.__name__} ({self.id})"