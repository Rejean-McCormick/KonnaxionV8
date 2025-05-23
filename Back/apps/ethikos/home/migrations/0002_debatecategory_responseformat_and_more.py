# Generated by Django 5.1.5 on 2025-05-07 13:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DebateCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "home_debatecategory",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ResponseFormat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("code", models.CharField(blank=True, max_length=50, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "home_responseformat",
                "ordering": ["id"],
            },
        ),
        migrations.AlterModelOptions(
            name="debatetopic",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="featureddebate",
            options={"ordering": ["display_order"]},
        ),
        migrations.AlterModelOptions(
            name="personalizedrecommendation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RemoveField(
            model_name="debatetopic",
            name="publish_date",
        ),
        migrations.RemoveField(
            model_name="debatetopic",
            name="title",
        ),
        migrations.AddField(
            model_name="debatetopic",
            name="options",
            field=models.JSONField(
                blank=True, help_text="Liste de valeurs pour choix multiples", null=True
            ),
        ),
        migrations.AddField(
            model_name="debatetopic",
            name="question",
            field=models.CharField(
                blank=True,
                help_text="Question du débat (peut être vide pour les anciens enregistrements)",
                max_length=500,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="debatetopic",
            name="scale_labels",
            field=models.JSONField(
                blank=True, help_text="Libellés des crans pour échelle", null=True
            ),
        ),
        migrations.AlterField(
            model_name="debatetopic",
            name="description",
            field=models.TextField(
                blank=True, help_text="Description optionnelle", null=True
            ),
        ),
        migrations.AlterField(
            model_name="debatetopic",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="featureddebate",
            name="active",
            field=models.BooleanField(
                default=True, help_text="Si ce sujet est actif/en avant"
            ),
        ),
        migrations.AlterField(
            model_name="featureddebate",
            name="debate_topic",
            field=models.ForeignKey(
                help_text="Sujet de débat mis en avant",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="featured_entries",
                to="home.debatetopic",
            ),
        ),
        migrations.AlterField(
            model_name="featureddebate",
            name="display_order",
            field=models.PositiveIntegerField(default=0, help_text="Ordre d'affichage"),
        ),
        migrations.AlterField(
            model_name="personalizedrecommendation",
            name="debate_topic",
            field=models.ForeignKey(
                help_text="Sujet recommandé",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recommendations",
                to="home.debatetopic",
            ),
        ),
        migrations.AlterField(
            model_name="personalizedrecommendation",
            name="score",
            field=models.FloatField(
                default=0, help_text="Score de pertinence de la recommandation"
            ),
        ),
        migrations.AlterField(
            model_name="personalizedrecommendation",
            name="user",
            field=models.ForeignKey(
                help_text="Utilisateur destinataire de la recommandation",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recommendations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="debatetopic",
            table="home_debatetopic",
        ),
        migrations.AlterModelTable(
            name="featureddebate",
            table="home_featureddebat",
        ),
        migrations.AlterModelTable(
            name="personalizedrecommendation",
            table="home_personalizedrecommendation",
        ),
        migrations.AddField(
            model_name="debatetopic",
            name="debatecategory",
            field=models.ForeignKey(
                blank=True,
                help_text="Catégorie du débat (nullable pour migration)",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="topics",
                to="home.debatecategory",
            ),
        ),
        migrations.CreateModel(
            name="PublicVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("value", models.CharField(max_length=255)),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="home.debatetopic",
                    ),
                ),
            ],
            options={
                "db_table": "home_publicvote",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="debatetopic",
            name="responseformat",
            field=models.ForeignKey(
                blank=True,
                help_text="Format de réponse (nullable pour migration)",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="topics",
                to="home.responseformat",
            ),
        ),
    ]
