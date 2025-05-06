-- 01_ddl_ethikos.sql
-- 1/4 – Création des tables de référentiel et adaptation de home_debatetopic

-- 1. Table des catégories de débat
CREATE TABLE IF NOT EXISTS home_debatecategory (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITHOUT TIME ZONE
);

-- 2. Table des formats de réponse
CREATE TABLE IF NOT EXISTS home_responseformat (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITHOUT TIME ZONE
);

-- 3. Adaptation de la table home_debatetopic
--    Ajout des colonnes manquantes pour les FK
ALTER TABLE home_debatetopic
  ADD COLUMN IF NOT EXISTS debatecategory_id BIGINT,
  ADD COLUMN IF NOT EXISTS responseformat_id BIGINT,
  ADD COLUMN IF NOT EXISTS created_by_id BIGINT;

-- 4. Création conditionnelle des contraintes
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'fk_home_debatetopic_debatecategory'
  ) THEN
    ALTER TABLE home_debatetopic
      ADD CONSTRAINT fk_home_debatetopic_debatecategory
        FOREIGN KEY (debatecategory_id)
        REFERENCES home_debatecategory(id)
        ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'fk_home_debatetopic_responseformat'
  ) THEN
    ALTER TABLE home_debatetopic
      ADD CONSTRAINT fk_home_debatetopic_responseformat
        FOREIGN KEY (responseformat_id)
        REFERENCES home_responseformat(id)
        ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'fk_home_debatetopic_created_by'
  ) THEN
    ALTER TABLE home_debatetopic
      ADD CONSTRAINT fk_home_debatetopic_created_by
        FOREIGN KEY (created_by_id)
        REFERENCES core_customuser(id)
        ON DELETE SET NULL;
  END IF;
END;
$$;
