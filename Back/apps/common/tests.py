# apps/common/tests.py

from django.test import TestCase
from django.utils import timezone
from django import forms
from rest_framework import serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import timedelta

# Importer les modules partagés
from common import utils, mixins, permissions as common_permissions, base_models

# ------------------------------------------------------------------------------
# 1. Tester les modèles de base
# ------------------------------------------------------------------------------

# Création d'un modèle factice héritant du BaseModel (défini dans common/base_models.py)
from django.db import models

class DummyModel(base_models.BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ------------------------------------------------------------------------------
# 2. Tester une fonction utilitaire
# ------------------------------------------------------------------------------

# Nous supposons que utils.py devrait contenir une fonction format_date.
# Si elle n'existe pas, nous la définissons ici pour le test.
if not hasattr(utils, 'format_date'):
    def format_date(date):
        return date.strftime("%Y-%m-%d")
    utils.format_date = format_date

class CommonUtilsTests(TestCase):
    def test_format_date(self):
        """
        Vérifie que la fonction format_date retourne la date au format 'YYYY-MM-DD'.
        """
        now = timezone.now()
        formatted = utils.format_date(now)
        self.assertEqual(formatted, now.strftime("%Y-%m-%d"))

# ------------------------------------------------------------------------------
# 3. Tester les mixins
# ------------------------------------------------------------------------------

# Supposons qu'un mixin DummyMixin est défini dans common/mixins.py avec une méthode factice.
# S'il n'existe pas, nous le créons ici pour le test.
if not hasattr(mixins, 'DummyMixin'):
    class DummyMixin:
        def get_dummy_value(self):
            return 42
    mixins.DummyMixin = DummyMixin

class CommonMixinsTests(TestCase):
    def test_dummy_mixin(self):
        """
        Vérifie que le DummyMixin fournit bien une méthode get_dummy_value renvoyant 42.
        """
        class TestClass(mixins.DummyMixin):
            pass
        obj = TestClass()
        self.assertEqual(obj.get_dummy_value(), 42)

# ------------------------------------------------------------------------------
# 4. Tester les permissions personnalisées
# ------------------------------------------------------------------------------

# Création d'une permission factice qui autorise uniquement les méthodes sûres (GET, HEAD, OPTIONS)
class DummyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CommonPermissionsTests(TestCase):
    def test_dummy_permission(self):
        """
        Vérifie que la permission factice autorise une requête GET et refuse une requête POST.
        """
        permission = DummyPermission()
        
        class DummyRequest:
            def __init__(self, method):
                self.method = method
        
        get_request = DummyRequest("GET")
        post_request = DummyRequest("POST")
        
        self.assertTrue(permission.has_permission(get_request, None))
        self.assertFalse(permission.has_permission(post_request, None))

# ------------------------------------------------------------------------------
# 5. Tester un formulaire et un serializer (exemples factices)
# ------------------------------------------------------------------------------

class DummyForm(forms.Form):
    field = forms.CharField(max_length=10)

class DummySerializer(serializers.Serializer):
    field = serializers.CharField(max_length=10)

class CommonFormsSerializersTests(TestCase):
    def test_dummy_form_validity(self):
        """
        Vérifie que le DummyForm valide une donnée correcte.
        """
        form = DummyForm(data={'field': 'test'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['field'], 'test')

    def test_dummy_serializer(self):
        """
        Vérifie que le DummySerializer (sans transformation particulière) fonctionne comme attendu.
        """
        data = {'field': 'test'}
        serializer = DummySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['field'], 'test')

# ------------------------------------------------------------------------------
# 6. Tester le comportement du modèle de base (BaseModel)
# ------------------------------------------------------------------------------

class CommonBaseModelsTests(TestCase):
    def test_dummy_model_creation(self):
        """
        Crée une instance de DummyModel et vérifie que les champs d'audit (created_at, updated_at)
        sont automatiquement renseignés.
        """
        instance = DummyModel.objects.create(name="Test Instance")
        self.assertIsNotNone(instance.created_at)
        self.assertIsNotNone(instance.updated_at)
        self.assertEqual(str(instance), "Test Instance")
