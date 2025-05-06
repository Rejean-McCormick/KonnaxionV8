#!/usr/bin/env python
import os
import django

# 1. Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendT.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import SystemConfiguration, ConfigurationChangelog
from ekoh.models import ExpertiseTag
from foundation.models import KnowledgeUnit
from projects.models import Project, Milestone, Task
from faker import Faker

def run():
    fake = Faker('fr_FR')
    User = get_user_model()

    # Configuration système minimale
    config, _ = SystemConfiguration.objects.get_or_create(
        key="site_title",
        defaults={"value": "Konnaxion Dev"}
    )
    ConfigurationChangelog.objects.get_or_create(
        configuration=config,
        defaults={"changed_by": None, "old_value": "", "new_value": config.value}
    )

    # Super-utilisateur unique
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="ChangeMe123!"
        )

    # Quelques tags d’expertise
    for _ in range(3):
        ExpertiseTag.objects.get_or_create(name=fake.word().capitalize())

    # Quelques unités de connaissance
    for _ in range(3):
        title = fake.sentence(nb_words=4).rstrip('.')
        KnowledgeUnit.objects.get_or_create(
            title=title,
            defaults={
                "description": fake.paragraph(nb_sentences=2),
                "content": fake.text(max_nb_chars=150)
            }
        )

    # Un projet, une milestone, une tâche
    admin = User.objects.filter(is_superuser=True).first()
    proj, _ = Project.objects.get_or_create(
        name="Projet de test",
        defaults={"description": "Test dummy data", "owner": admin}
    )
    ms, _ = Milestone.objects.get_or_create(
        project=proj,
        name="Milestone 1",
        defaults={"due_date": fake.future_date(end_date="+10d")}
    )
    Task.objects.get_or_create(
        milestone=ms,
        title="Tâche 1",
        defaults={"description": "Description test", "assigned_to": admin, "status": "todo"}
    )

    print("✅ Dummy data injecté avec succès.")

if __name__ == "__main__":
    run()
