-- dbethikos2.sql
-- 1) Insertion des catégories initiales (évite doublons par nom)
INSERT INTO home_debatecategory (name, created_at, updated_at, is_deleted, deleted_at)
SELECT v.name, NOW(), NOW(), FALSE, NULL
FROM (
  VALUES
    ('Governance, Democracy & Political Reform'),
    ('Economy & Taxation'),
    ('Employment & Labor Rights'),
    ('Housing & Urban Development'),
    ('Environment & Climate Change'),
    ('Energy & Natural Resources'),
    ('Healthcare & Public Health'),
    ('Immigration & Refugee Policy'),
    ('Indigenous Rights & Reconciliation'),
    ('Crime & Policing'),
    ('Digital Privacy, AI & Cybersecurity'),
    ('Transportation & Infrastructure'),
    ('Foreign Policy & National Security'),
    ('Media, Culture & National Identity')
) AS v(name)
WHERE NOT EXISTS (
  SELECT 1
    FROM home_debatecategory c
   WHERE c.name = v.name
);

-- 2) Insertion des formats de réponse (évite doublons par nom)
INSERT INTO home_responseformat (name, description, created_at, updated_at, is_deleted, deleted_at)
SELECT v.name, v.description, NOW(), NOW(), FALSE, NULL
FROM (
  VALUES
    ('binary',  'Yes/No (with optional Abstain)'),
    ('scale_5', '5-point scale from very unfavorable to very favorable')
) AS v(name, description)
WHERE NOT EXISTS (
  SELECT 1
    FROM home_responseformat r
   WHERE r.name = v.name
);

-- 3) Création de l'utilisateur fictif KingKlown (évite doublons par username)
INSERT INTO core_customuser (
    username,
    password,
    last_login,
    is_superuser,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    language_preference,
    device_details,
    role,
    offline_sync_token,
    created_at,
    updated_at,
    is_deleted,
    deleted_at
)
SELECT
    v.username,
    v.password,
    NULL,
    FALSE,
    v.first_name,
    v.last_name,
    v.email,
    FALSE,
    TRUE,
    NOW(),
    'en',
    NULL,
    'user',
    NULL,
    NOW(),
    NOW(),
    FALSE,
    NULL
FROM (
  VALUES
    ('KingKlown', '!', 'King', 'Klown', 'kingklown@example.com')
) AS v(username, password, first_name, last_name, email)
WHERE NOT EXISTS (
  SELECT 1
    FROM core_customuser u
   WHERE u.username = v.username
);
