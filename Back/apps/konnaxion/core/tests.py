# apps/konnaxion/core/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model

# Importez les modèles depuis l'app core
from konnaxion.core.models import SystemConfiguration, ConfigurationChangeLog

User = get_user_model()

class CustomUserModelTests(TestCase):
    def test_create_custom_user(self):
        """
        Teste la création d'un utilisateur personnalisé.
        Vérifie que les champs essentiels (username, email, préférence de langue) sont correctement enregistrés.
        """
        user = User.objects.create_user(
            username="utilisateur_test",
            password="motdepasse123",
            email="test@example.com"
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "utilisateur_test")
        self.assertEqual(user.email, "test@example.com")
        # Vérifier la valeur par défaut de la préférence de langue (par exemple, "en")
        self.assertEqual(user.language_preference, "en")


class SystemConfigurationModelTests(TestCase):
    def test_create_system_configuration(self):
        """
        Teste la création d'une configuration système.
        Vérifie que la clé et la valeur sont correctement enregistrées.
        """
        config = SystemConfiguration.objects.create(
            key="CONFIG_TEST",
            value='{"enabled": true}'
        )
        self.assertEqual(config.key, "CONFIG_TEST")
        self.assertIn("enabled", config.value)


class ConfigurationChangeLogModelTests(TestCase):
    def setUp(self):
        """
        Prépare les données de test en créant un utilisateur et une configuration système.
        """
        self.user = User.objects.create_user(
            username="changeur",
            password="motdepasse456",
            email="changeur@example.com"
        )
        self.config = SystemConfiguration.objects.create(
            key="CONFIG_CHANGE",
            value="1"
        )

    def test_create_configuration_change_log(self):
        """
        Teste la création d'un log de changement de configuration.
        Vérifie que la relation avec la configuration et l'utilisateur est correcte,
        ainsi que les valeurs d'ancien et de nouveau paramètre.
        """
        log = ConfigurationChangeLog.objects.create(
            configuration=self.config,
            old_value="1",
            new_value="2",
            changed_by=self.user,
            change_reason="Modification de test"
        )
        self.assertEqual(log.configuration, self.config)
        self.assertEqual(log.old_value, "1")
        self.assertEqual(log.new_value, "2")
        self.assertEqual(log.changed_by, self.user)
        self.assertEqual(log.change_reason, "Modification de test")
