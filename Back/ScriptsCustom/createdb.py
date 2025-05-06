#!/usr/bin/env python3
"""
This script creates a PostgreSQL database called "konnaxion" (if it does not already exist)
and then, within that database, creates multiple schemas and tables with enriched definitions.
Schemas include:
  - hub_commun: Central shared data (global users, activity logs, global parameters)
  - konnected: Educational data (users, exam responses, educational paths, certified skills)
  - keenkonnect: Collaborative projects (projects, project phases, external resources, collaborators)
  - ethikos: Ethical debates (debates, proposals/arguments, votes, comments, analytic summaries)
  - kreative: Artistic data (artworks, artists/creators, exhibitions/portfolios, collaborations, reviews)
  - ekoh: Evaluation and weighting (accomplishments, real-life achievements, goals/interests, global scores, evaluation history)
Each table has been enriched with additional columns (e.g. audit fields, categorization, status fields) as an expert might design.
"""

import os
import psycopg2
from psycopg2 import sql

# Connection parameters (can be configured via environment variables)
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_SUPERUSER = os.environ.get("POSTGRES_USER", "konnaxion_user")
DB_SUPERUSER_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "Gr05bo55")
TARGET_DB = os.environ.get("TARGET_DB", "konnaxion")

# Define the order in which schemas should be created (dependencies first)
schema_order = [
    "hub_commun",
    "konnected",
    "keenkonnect",
    "ethikos",
    "kreative",
    "ekoh"
]

# Define enriched DDL commands for each schema and its tables.
schemas = {
    "hub_commun": {
        "description": "Central hub for cross-cutting data",
        "ddl": [
            # Global Users
            """
            CREATE TABLE IF NOT EXISTS hub_commun.utilisateurs_globaux (
                id BIGSERIAL PRIMARY KEY,
                identifiant_unique VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(254) NOT NULL UNIQUE,
                nom_complet VARCHAR(255),
                preferences JSONB,
                lien_module VARCHAR(500),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                dernier_acces TIMESTAMP,
                statut VARCHAR(50)
            );
            """,
            # Activity Logs
            """
            CREATE TABLE IF NOT EXISTS hub_commun.logs_activite (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                action VARCHAR(255) NOT NULL,
                date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details JSONB,
                ip_adresse INET,
                session_id VARCHAR(100),
                appareil VARCHAR(100),
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Global Parameters
            """
            CREATE TABLE IF NOT EXISTS hub_commun.parametres_globaux (
                id BIGSERIAL PRIMARY KEY,
                cle VARCHAR(255) NOT NULL UNIQUE,
                valeur JSONB NOT NULL,
                description TEXT,
                categorie VARCHAR(50),
                actif BOOLEAN DEFAULT TRUE
            );
            """
        ]
    },
    "konnected": {
        "description": "Educational data and certification",
        "ddl": [
            # Educational Users
            """
            CREATE TABLE IF NOT EXISTS konnected.utilisateurs (
                id BIGSERIAL PRIMARY KEY,
                nom_utilisateur VARCHAR(150) NOT NULL UNIQUE,
                email VARCHAR(254) NOT NULL UNIQUE,
                mot_de_passe_hash VARCHAR(255),
                photo_profil VARCHAR(500),
                profil TEXT,
                age INTEGER,
                niveau VARCHAR(50),
                preferences JSONB,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut VARCHAR(50)
            );
            """,
            # Exam Responses
            """
            CREATE TABLE IF NOT EXISTS konnected.reponses_examen (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                question_id INTEGER,
                reponse TEXT NOT NULL,
                score_obtenu DECIMAL,
                question_difficulte INTEGER,
                correction TEXT,
                date_submission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES konnected.utilisateurs(id)
            );
            """,
            # Educational Path
            """
            CREATE TABLE IF NOT EXISTS konnected.parcours_educatif (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                cours VARCHAR(255),
                progression DECIMAL,
                etat VARCHAR(50),
                note_finale DECIMAL,
                date_commencement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_achevement TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES konnected.utilisateurs(id)
            );
            """,
            # Certified Skills
            """
            CREATE TABLE IF NOT EXISTS konnected.habilites_attestees (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                competence VARCHAR(255) NOT NULL,
                organisme_certifiant VARCHAR(255),
                date_certification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_expiration TIMESTAMP,
                niveau_certification VARCHAR(50),
                FOREIGN KEY (utilisateur_id) REFERENCES konnected.utilisateurs(id)
            );
            """
        ]
    },
    "keenkonnect": {
        "description": "Collaborative projects",
        "ddl": [
            # Projects
            """
            CREATE TABLE IF NOT EXISTS keenkonnect.projets (
                id BIGSERIAL PRIMARY KEY,
                titre VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                description_complete TEXT,
                proprietaire_id INTEGER,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut VARCHAR(50),
                FOREIGN KEY (proprietaire_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Project Phases
            """
            CREATE TABLE IF NOT EXISTS keenkonnect.etapes_projet (
                id BIGSERIAL PRIMARY KEY,
                projet_id INTEGER NOT NULL,
                nom_etape VARCHAR(255),
                ordre INTEGER NOT NULL,
                description TEXT,
                date_debut TIMESTAMP,
                date_fin TIMESTAMP,
                statut VARCHAR(50),
                FOREIGN KEY (projet_id) REFERENCES keenkonnect.projets(id),
                UNIQUE (projet_id, ordre)
            );
            """,
            # External Resources
            """
            CREATE TABLE IF NOT EXISTS keenkonnect.ressources_externes (
                id BIGSERIAL PRIMARY KEY,
                etape_id INTEGER NOT NULL,
                type_ressource VARCHAR(50),
                url VARCHAR(500) NOT NULL,
                description TEXT,
                taille_fichier INTEGER,
                format VARCHAR(50),
                FOREIGN KEY (etape_id) REFERENCES keenkonnect.etapes_projet(id)
            );
            """,
            # Collaborators
            """
            CREATE TABLE IF NOT EXISTS keenkonnect.collaborateurs (
                id BIGSERIAL PRIMARY KEY,
                projet_id INTEGER NOT NULL,
                utilisateur_id INTEGER NOT NULL,
                role_collaborateur VARCHAR(50),
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (projet_id, utilisateur_id),
                FOREIGN KEY (projet_id) REFERENCES keenkonnect.projets(id)
            );
            """
        ]
    },
    "ethikos": {
        "description": "Ethical debates",
        "ddl": [
            # Debates
            """
            CREATE TABLE IF NOT EXISTS ethikos.debats (
                id BIGSERIAL PRIMARY KEY,
                theme VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                categorie VARCHAR(50),
                moderateur_id INTEGER,
                etat_debat VARCHAR(50),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_lancement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut VARCHAR(50),
                FOREIGN KEY (moderateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Proposals/Arguments
            """
            CREATE TABLE IF NOT EXISTS ethikos.propositions_arguments (
                id BIGSERIAL PRIMARY KEY,
                debat_id INTEGER NOT NULL,
                auteur_id INTEGER NOT NULL,
                texte TEXT NOT NULL,
                parent_id INTEGER,
                score DECIMAL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (debat_id) REFERENCES ethikos.debats(id)
            );
            """,
            # Votes
            """
            CREATE TABLE IF NOT EXISTS ethikos.votes (
                id BIGSERIAL PRIMARY KEY,
                proposition_id INTEGER NOT NULL,
                utilisateur_id INTEGER NOT NULL,
                valeur CHAR(2) NOT NULL CHECK (valeur IN ('UP','DN')),
                ip_vote INET,
                date_vote TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (proposition_id, utilisateur_id),
                FOREIGN KEY (proposition_id) REFERENCES ethikos.propositions_arguments(id)
            );
            """,
            # Comments
            """
            CREATE TABLE IF NOT EXISTS ethikos.commentaires (
                id BIGSERIAL PRIMARY KEY,
                proposition_id INTEGER NOT NULL,
                auteur_id INTEGER NOT NULL,
                contenu TEXT NOT NULL,
                parent_commentaire_id INTEGER,
                modere BOOLEAN DEFAULT FALSE,
                date_commentaire TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (proposition_id) REFERENCES ethikos.propositions_arguments(id)
            );
            """,
            # Analytic Summaries
            """
            CREATE TABLE IF NOT EXISTS ethikos.synthese_analytique (
                id BIGSERIAL PRIMARY KEY,
                debat_id INTEGER NOT NULL,
                taux_consensus DECIMAL,
                resume TEXT,
                score_moyen DECIMAL,
                nombre_participants INTEGER,
                date_aggregation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (debat_id) REFERENCES ethikos.debats(id)
            );
            """
        ]
    },
    "kreative": {
        "description": "Artistic and cultural data",
        "ddl": [
            # Artworks
            """
            CREATE TABLE IF NOT EXISTS kreative.oeuvres (
                id BIGSERIAL PRIMARY KEY,
                titre VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                url_fichier VARCHAR(500) NOT NULL,
                thumbnail_url VARCHAR(500),
                metadonnees JSONB,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                style VARCHAR(100),
                tags JSONB
            );
            """,
            # Artists/Creators
            """
            CREATE TABLE IF NOT EXISTS kreative.artistes_createurs (
                id BIGSERIAL PRIMARY KEY,
                nom VARCHAR(255) NOT NULL,
                biographie TEXT,
                biographie_complete TEXT,
                date_naissance DATE,
                nationalite VARCHAR(100),
                coordonnees JSONB,
                site_web VARCHAR(500)
            );
            """,
            # Exhibitions/Portfolios
            """
            CREATE TABLE IF NOT EXISTS kreative.expositions_portfolios (
                id BIGSERIAL PRIMARY KEY,
                titre VARCHAR(255) NOT NULL,
                description TEXT,
                lieu VARCHAR(255),
                date_exposition TIMESTAMP,
                date_debut TIMESTAMP,
                date_fin TIMESTAMP,
                organisateur VARCHAR(255)
            );
            """,
            # Collaborations
            """
            CREATE TABLE IF NOT EXISTS kreative.collaborations (
                id BIGSERIAL PRIMARY KEY,
                oeuvre_id INTEGER NOT NULL,
                artiste_id INTEGER NOT NULL,
                role_collaboration VARCHAR(50),
                date_debut TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (oeuvre_id, artiste_id),
                FOREIGN KEY (oeuvre_id) REFERENCES kreative.oeuvres(id),
                FOREIGN KEY (artiste_id) REFERENCES kreative.artistes_createurs(id)
            );
            """,
            # Comments and Evaluations
            """
            CREATE TABLE IF NOT EXISTS kreative.commentaires_evaluations (
                id BIGSERIAL PRIMARY KEY,
                oeuvre_id INTEGER NOT NULL,
                utilisateur_id INTEGER NOT NULL,
                contenu TEXT NOT NULL,
                note DECIMAL,
                note_evaluation DECIMAL,
                modere BOOLEAN DEFAULT FALSE,
                date_commentaire TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (oeuvre_id) REFERENCES kreative.oeuvres(id)
            );
            """
        ]
    },
    "ekoh": {
        "description": "Evaluation and weighting of accomplishments",
        "ddl": [
            # Accomplishments from Konnected
            """
            CREATE TABLE IF NOT EXISTS ekoh.accomplissements_konnected (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                certification VARCHAR(255),
                score_examen DECIMAL,
                date_obtention TIMESTAMP,
                date_validation TIMESTAMP,
                organisme_certifiant VARCHAR(255),
                commentaire TEXT,
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Real-life Achievements
            """
            CREATE TABLE IF NOT EXISTS ekoh.realisations_reelles (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                honneur VARCHAR(255),
                medaille VARCHAR(255),
                date_reconnaissance TIMESTAMP,
                type_recompense VARCHAR(50),
                organisme_attribuant VARCHAR(255),
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Goals and Interests
            """
            CREATE TABLE IF NOT EXISTS ekoh.objectifs_interets (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                objectif TEXT,
                interet TEXT,
                categorie_objectif VARCHAR(50),
                priorite INTEGER,
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Global Score Profile
            """
            CREATE TABLE IF NOT EXISTS ekoh.scores_profil_global (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                score_global DECIMAL,
                details_scores JSONB,
                version INTEGER DEFAULT 1,
                date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """,
            # Evaluation History
            """
            CREATE TABLE IF NOT EXISTS ekoh.historique_evaluation (
                id BIGSERIAL PRIMARY KEY,
                utilisateur_id INTEGER NOT NULL,
                score_global DECIMAL,
                commentaire_evaluation TEXT,
                date_evaluation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES hub_commun.utilisateurs_globaux(id)
            );
            """
        ]
    }
}

# Function to grant rights on a schema
def grant_schema_rights(conn, schema, role):
    grant_commands = [
        sql.SQL("GRANT USAGE ON SCHEMA {} TO {};").format(sql.Identifier(schema), sql.Identifier(role)),
        sql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {} TO {};").format(sql.Identifier(schema), sql.Identifier(role))
    ]
    cur = conn.cursor()
    for cmd in grant_commands:
        try:
            cur.execute(cmd)
            print(f"[{schema}] Granted rights with: {cmd.as_string(conn)}")
        except Exception as e:
            print(f"[{schema}] Error granting rights: {e}\nCommand: {cmd.as_string(conn)}")
    cur.close()

# Execute a given SQL command
def execute_command(conn, command, schema_name=None):
    cur = conn.cursor()
    try:
        cur.execute(command)
        if schema_name:
            first_line = command.strip().splitlines()[0]
            print(f"[{schema_name}] Executed: {first_line}")
        else:
            print(f"Executed: {command.strip().splitlines()[0]}")
    except Exception as e:
        print(f"Error executing command: {e}\nCommand: {command}")
    cur.close()

# Create the target database if it does not exist
def create_database_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_SUPERUSER,
            password=DB_SUPERUSER_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TARGET_DB,))
        exists = cur.fetchone()
        if exists:
            print(f"Database '{TARGET_DB}' already exists.")
        else:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TARGET_DB)))
            print(f"Database '{TARGET_DB}' created successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database '{TARGET_DB}': {e}")

def main():
    # 1. Create the target database if needed
    create_database_if_not_exists()

    # 2. Connect to the target database ("konnaxion")
    try:
        conn = psycopg2.connect(
            dbname=TARGET_DB,
            user=DB_SUPERUSER,
            password=DB_SUPERUSER_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        print(f"Connected to database '{TARGET_DB}'.")
    except Exception as e:
        print(f"Error connecting to database '{TARGET_DB}': {e}")
        return

    # 3. Create schemas in the required order
    cur = conn.cursor()
    for schema in schema_order:
        try:
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema)))
            print(f"Schema '{schema}' created or already exists.")
        except Exception as e:
            print(f"Error creating schema '{schema}': {e}")
    cur.close()

    # 4. Execute the enriched DDL commands for each schema
    for schema in schema_order:
        module = schemas.get(schema)
        if module:
            print(f"Configuring schema '{schema}' ({module['description']})...")
            for ddl in module["ddl"]:
                execute_command(conn, ddl, schema_name=schema)
        else:
            print(f"No DDL defined for schema '{schema}'.")

    # 5. Grant rights on each schema to the application role
    for schema in schema_order:
        grant_schema_rights(conn, schema, DB_SUPERUSER)

    conn.close()
    print("All schemas, tables, and privileges have been created.")

if __name__ == '__main__':
    main()
