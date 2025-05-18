# apps/ethikos/home/models.py

from django.db import models
from django.conf import settings
from common.base_models import BaseModel

class DebateCategory(BaseModel):
    """
    Catégories de questions (ex. Politique, Éthique, Environnement…).
    """
    name = models.CharField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "home_debatecategory"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ResponseFormat(BaseModel):
    """
    Formats de réponse possibles (binaire, échelle, choix multiples…).
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "home_responseformat"
        ordering = ["id"]

    def __str__(self):
        return self.name


class DebateTopic(BaseModel):
    """
    Sujet de débat ouvert au vote public.
    """
    question = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Question du débat (peut être vide pour les anciens enregistrements)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description optionnelle"
    )
    debatecategory = models.ForeignKey(
        DebateCategory,
        on_delete=models.CASCADE,
        related_name="topics",
        null=True,
        blank=True,
        help_text="Catégorie du débat (nullable pour migration)"
    )
    responseformat = models.ForeignKey(
        ResponseFormat,
        on_delete=models.CASCADE,
        related_name="topics",
        null=True,    # rendu nullable pour ne pas exiger de default
        blank=True,
        help_text="Format de réponse (nullable pour migration)"
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    options = models.JSONField(
        blank=True, null=True,
        help_text="Liste de valeurs pour choix multiples"
    )
    scale_labels = models.JSONField(
        blank=True, null=True,
        help_text="Libellés des crans pour échelle"
    )

    class Meta:
        db_table = "home_debatetopic"
        ordering = ["-created_at"]

    def __str__(self):
        return self.question or "(question non spécifiée)"

    @property
    def turnout(self):
        # Nombre total de votes (à adapter selon logique métier)
        return self.votes.count()


class FeaturedDebate(BaseModel):
    """
    Marque un sujet de débat comme mis en avant.
    """
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="featured_entries",
        help_text="Sujet de débat mis en avant"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Ordre d'affichage"
    )
    active = models.BooleanField(
        default=True,
        help_text="Si ce sujet est actif/en avant"
    )

    class Meta:
        db_table = "home_featureddebat"
        ordering = ["display_order"]

    def __str__(self):
        return f"Featured: {self.debate_topic}"


class PersonalizedRecommendation(BaseModel):
    """
    Stocke une recommandation personnalisée pour un utilisateur.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Utilisateur destinataire de la recommandation"
    )
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Sujet recommandé"
    )
    score = models.FloatField(
        default=0,
        help_text="Score de pertinence de la recommandation"
    )

    class Meta:
        db_table = "home_personalizedrecommendation"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recommendation for {self.user}: {self.debate_topic}"


class PublicVote(BaseModel):
    """
    Enregistrement d’un vote public sur un sujet.
    """
    topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "home_publicvote"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Vote {self.value} sur '{self.topic}'"
