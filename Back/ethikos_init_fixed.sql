-- Insertion des catÃ©gories initiales (Ã©vite doublons par nom)
INSERT INTO home_debatecategory (name, created_at, updated_at, is_deleted, deleted_at)
SELECT v.name, NOW(), NOW(), FALSE, NULL
FROM (VALUES
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
    SELECT 1 FROM home_debatecategory c WHERE c.name = v.name
);
-- CrÃ©ation de la table des formats de rÃ©ponse (si non existante)
CREATE TABLE IF NOT EXISTS home_responseformat (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE
);
-- Insertion des formats de rÃ©ponse disponibles (Ã©vite doublons par nom)
INSERT INTO home_responseformat (name, description, created_at, updated_at, is_deleted, deleted_at)
SELECT vals.name, vals.description, NOW(), NOW(), FALSE, NULL
FROM (VALUES
    ('binary', 'Yes/No (with optional Abstain)'),
    ('scale_5', '5-point scale from very unfavorable to very favorable')
) AS vals(name, description)
WHERE NOT EXISTS (
    SELECT 1 FROM home_responseformat r WHERE r.name = vals.name
);
-- CrÃ©ation de l'utilisateur fictif "King Klown" (valeurs par dÃ©faut pour champs requis)
INSERT INTO core_customuser (username, password, last_login, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined, language_preference, device_details, role, offline_sync_token, created_at, updated_at, is_deleted, deleted_at)
SELECT 'KingKlown', '!', NULL, FALSE, 'King', 'Klown', 'king.klown@example.com', FALSE, TRUE, NOW(), 'en', NULL, 'user', NULL, NOW(), NOW(), FALSE, NULL
WHERE NOT EXISTS (
    SELECT 1 FROM core_customuser u WHERE u.username = 'KingKlown'
);
-- Insertion des questions de dÃ©bat initiales, avec association Ã  la catÃ©gorie et au format correspondants.
-- Chaque insertion utilise une sous-requÃªte pour rÃ©cupÃ©rer les IDs de category, format et user, et Ã©vite les doublons de titre.
-- 1. U.S. Tariffs & Canadaâ€™s Response
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada negotiate sector-based exemptions from U.S. tariffs rather than retaliating with tariffs on U.S. goods?',
    'U.S. plans a 25% tariff on Canadian imports; Canada is considering retaliation.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation' 
  AND fmt.name = 'scale_5'    -- multiple options (negotiate vs retaliate vs no action)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada negotiate sector-based exemptions from U.S. tariffs rather than retaliating with tariffs on U.S. goods?' 
        AND d.is_deleted = FALSE
  );
-- 1. (suite) Trade strategy if U.S. tariffs proceed
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'If the U.S. proceeds with a 25% tariff on all Canadian imports, which approach should Canada prioritize?',
    'U.S. imposes broad tariffs on Canada â€“ possible response strategies for Canada.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation'
  AND fmt.name = 'scale_5'    -- plusieurs choix stratÃ©giques (diversifier accords, soutenir industries locales, etc.)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'If the U.S. proceeds with a 25% tariff on all Canadian imports, which approach should Canada prioritize?' 
        AND d.is_deleted = FALSE
  );
-- 2. Electoral System & Democracy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada move to a proportional representation voting system to better reflect diverse political views?',
    'Upcoming federal elections and potential changes to the voting system.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND fmt.name = 'binary'    -- oui/non (changer de systÃ¨me ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada move to a proportional representation voting system to better reflect diverse political views?' 
        AND d.is_deleted = FALSE
  );
-- 2. (suite) Online voting accessibility
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada implement online voting in federal elections to increase accessibility?',
    'Upcoming federal elections and potential changes to the voting system.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND fmt.name = 'scale_5'    -- 3 options (yes for all, yes limited, no)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada implement online voting in federal elections to increase accessibility?' 
        AND d.is_deleted = FALSE
  );
-- 3. Environment & Energy Policy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada stop approving new fossil fuel projects by 2030?',
    'Canadaâ€™s transition to a clean energy economy while balancing economic needs.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Environment & Climate Change'
  AND fmt.name = 'binary'    -- oui/non (arrÃªter ou non les nouveaux projets fossiles)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada stop approving new fossil fuel projects by 2030?' 
        AND d.is_deleted = FALSE
  );
-- 3. (suite) Financing green transition
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'How should Canada finance the transition to a green economy?',
    'Canadaâ€™s transition to a clean energy economy while balancing economic needs.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Environment & Climate Change'
  AND fmt.name = 'scale_5'    -- plusieurs options (carbon pricing, redirect subsidies, private investment)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'How should Canada finance the transition to a green economy?' 
        AND d.is_deleted = FALSE
  );
-- 3. (suite) Single-use plastics ban
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada ban single-use plastics completely within the next five years?',
    'Canadaâ€™s transition to a clean energy economy while balancing economic needs.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Environment & Climate Change'
  AND fmt.name = 'binary'    -- oui/non (banir ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada ban single-use plastics completely within the next five years?' 
        AND d.is_deleted = FALSE
  );
-- 4. Food Safety & Public Health
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should food import regulations be strengthened to prevent contaminated products from entering Canada?',
    'Rise in salmonella cases due to contaminated food imports.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (renforcer les contrÃ´les ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should food import regulations be strengthened to prevent contaminated products from entering Canada?' 
        AND d.is_deleted = FALSE
  );
-- 4. (suite) Penalties for foodborne illness outbreaks
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should companies responsible for foodborne illness outbreaks face increased financial penalties?',
    'Rise in salmonella cases due to contaminated food imports.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (sanctions accrues ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should companies responsible for foodborne illness outbreaks face increased financial penalties?' 
        AND d.is_deleted = FALSE
  );
-- 5. Education & Youth Well-being
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should all public high schools be required to provide mental health education?',
    'Mental health programs in schools have been shown to reduce youth drug use.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (obligatoire ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should all public high schools be required to provide mental health education?' 
        AND d.is_deleted = FALSE
  );
-- 5. (suite) Addressing youth drug use
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'How should the government address youth drug use prevention?',
    'Mental health programs in schools have been shown to reduce youth drug use.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'scale_5'    -- plusieurs options (expand programs, rehab access, tougher penalties)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'How should the government address youth drug use prevention?' 
        AND d.is_deleted = FALSE
  );
-- 6. Housing Crisis & Affordability
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada impose stricter regulations on foreign real estate investors to cool down the housing market?',
    'Rising housing costs and affordability issues in Canadaâ€™s major cities.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Housing & Urban Development'
  AND fmt.name = 'scale_5'    -- 3 options (ban foreign buyers, tax them, or laissez-faire)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada impose stricter regulations on foreign real estate investors to cool down the housing market?' 
        AND d.is_deleted = FALSE
  );
-- 6. (suite) Public housing investment
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government invest more in public housing projects?',
    'Rising housing costs and affordability issues in Canadaâ€™s major cities.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Housing & Urban Development'
  AND fmt.name = 'binary'    -- oui/non (investir davantage ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government invest more in public housing projects?' 
        AND d.is_deleted = FALSE
  );
-- 7. Immigration & Refugee Policy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada prioritize skilled immigration over other types of immigration?',
    'Debates over Canadaâ€™s immigration system and labor shortages.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (prioriser les immigrants Ã©conomiques ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada prioritize skilled immigration over other types of immigration?' 
        AND d.is_deleted = FALSE
  );
-- 7. (suite) Speed up refugee processing
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should refugee claim processing be sped up to reduce backlog issues?',
    'Debates over Canadaâ€™s immigration system and labor shortages.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (accÃ©lÃ©rer les procÃ©dures ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should refugee claim processing be sped up to reduce backlog issues?' 
        AND d.is_deleted = FALSE
  );
-- 8. Crime & Policing
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada increase funding for police forces to combat rising crime?',
    'Rising crime rates in urban areas and debates on police funding.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Crime & Policing'
  AND fmt.name = 'binary'    -- oui/non (augmenter les fonds de police ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada increase funding for police forces to combat rising crime?' 
        AND d.is_deleted = FALSE
  );
-- 8. (suite) Decriminalize drug possession
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada decriminalize drug possession for personal use and focus on rehabilitation instead of punishment?',
    'Rising crime rates in urban areas and debates on police funding.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Crime & Policing'
  AND fmt.name = 'binary'    -- oui/non (dÃ©criminaliser ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada decriminalize drug possession for personal use and focus on rehabilitation instead of punishment?' 
        AND d.is_deleted = FALSE
  );
-- 9. Foreign Policy & Defense
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada increase defense spending to meet NATO\'s 2% GDP target?',
    'Canadaâ€™s military spending and global security commitments.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (augmenter les dÃ©penses de dÃ©fense ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada increase defense spending to meet NATO''s 2% GDP target?' 
        AND d.is_deleted = FALSE
  );
-- 9. (suite) Human rights vs trade
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada take a stronger stance against human rights violations in foreign countries, even if it affects trade?',
    'Canadaâ€™s military spending and global security commitments.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (prioriser droits humains ou intÃ©rÃªts Ã©conomiques)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada take a stronger stance against human rights violations in foreign countries, even if it affects trade?' 
        AND d.is_deleted = FALSE
  );
-- 10. Taxation & Economy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada introduce a wealth tax on individuals with assets exceeding $10 million?',
    'Corporate taxation, government spending, and cost-of-living issues.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation'
  AND fmt.name = 'binary'    -- oui/non (instaurer un impÃ´t sur la fortune ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada introduce a wealth tax on individuals with assets exceeding $10 million?' 
        AND d.is_deleted = FALSE
  );
-- 10. (suite) GST reduction
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada reduce the Goods and Services Tax (GST) to lower the cost of living?',
    'Corporate taxation, government spending, and cost-of-living issues.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation'
  AND fmt.name = 'binary'    -- oui/non (rÃ©duire la TPS ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada reduce the Goods and Services Tax (GST) to lower the cost of living?' 
        AND d.is_deleted = FALSE
  );
-- 10. (suite) Price controls for inflation
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada impose price controls on essential goods (groceries, housing, fuel) to combat inflation?',
    'Corporate taxation, government spending, and cost-of-living issues.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation'
  AND fmt.name = 'binary'    -- oui/non (contrÃ´ler les prix ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada impose price controls on essential goods (groceries, housing, fuel) to combat inflation?' 
        AND d.is_deleted = FALSE
  );
-- 10. (suite) Universal Basic Income (UBI)
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada introduce universal basic income (UBI) as a replacement for some welfare programs?',
    'Corporate taxation, government spending, and cost-of-living issues.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Economy & Taxation'
  AND fmt.name = 'binary'    -- oui/non (introduire un RBI ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada introduce universal basic income (UBI) as a replacement for some welfare programs?' 
        AND d.is_deleted = FALSE
  );
-- 11. Transportation & Infrastructure
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada build a national high-speed rail system linking major cities (e.g., Toronto-Montreal, Calgary-Edmonton)?',
    'Public transit, high-speed rail, and sustainable transportation.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Transportation & Infrastructure'
  AND fmt.name = 'binary'    -- oui/non (construire un TGV national ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada build a national high-speed rail system linking major cities (e.g., Toronto-Montreal, Calgary-Edmonton)?' 
        AND d.is_deleted = FALSE
  );
-- 11. (suite) Gas-powered vehicle ban
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should gas-powered cars be banned for sale by 2035 in favor of electric vehicles (EVs)?',
    'Public transit, high-speed rail, and sustainable transportation.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Transportation & Infrastructure'
  AND fmt.name = 'binary'    -- oui/non (interdire les autos essence dÃ¨s 2035 ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should gas-powered cars be banned for sale by 2035 in favor of electric vehicles (EVs)?' 
        AND d.is_deleted = FALSE
  );
-- 11. (suite) Free public transit in cities
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should all major Canadian cities provide free public transit?',
    'Public transit, high-speed rail, and sustainable transportation.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Transportation & Infrastructure'
  AND fmt.name = 'scale_5'    -- plusieurs options (gratuit, subventionnÃ©, payant)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should all major Canadian cities provide free public transit?' 
        AND d.is_deleted = FALSE
  );
-- 12. Digital Privacy & Technology
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada ban companies from using facial recognition technology in public spaces?',
    'AI regulation, government surveillance, and online safety.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Digital Privacy, AI & Cybersecurity'
  AND fmt.name = 'binary'    -- oui/non (interdire la reconnaissance faciale ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada ban companies from using facial recognition technology in public spaces?' 
        AND d.is_deleted = FALSE
  );
-- 12. (suite) Social media responsibility for misinformation
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should social media companies be legally responsible for stopping misinformation on their platforms?',
    'AI regulation, government surveillance, and online safety.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Digital Privacy, AI & Cybersecurity'
  AND fmt.name = 'binary'    -- oui/non (responsabiliser lÃ©galement les rÃ©seaux sociaux ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should social media companies be legally responsible for stopping misinformation on their platforms?' 
        AND d.is_deleted = FALSE
  );
-- 12. (suite) Government-run social media
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada create its own government-run social media platform to ensure fair public discourse?',
    'AI regulation, government surveillance, and online safety.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Digital Privacy, AI & Cybersecurity'
  AND fmt.name = 'binary'    -- oui/non (crÃ©er un rÃ©seau social public ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada create its own government-run social media platform to ensure fair public discourse?' 
        AND d.is_deleted = FALSE
  );
-- 12. (suite) Labeling AI-generated content
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should AI-generated content (news, images, videos) be required to carry a label indicating it\'s artificial?',
    'AI regulation, government surveillance, and online safety.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Digital Privacy, AI & Cybersecurity'
  AND fmt.name = 'binary'    -- oui/non (imposer un Ã©tiquetage des contenus IA ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should AI-generated content (news, images, videos) be required to carry a label indicating it''s artificial?' 
        AND d.is_deleted = FALSE
  );
-- 13. Foreign Ownership & Economic Sovereignty
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada ban foreign buyers from purchasing residential real estate permanently?',
    'Protection of Canadian industries and real estate from foreign influence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Housing & Urban Development'
  AND fmt.name = 'binary'    -- oui/non (bannir dÃ©finitivement les acheteurs Ã©trangers ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada ban foreign buyers from purchasing residential real estate permanently?' 
        AND d.is_deleted = FALSE
  );
-- 13. (suite) Blocking foreign takeovers of energy firms
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government prevent foreign companies from buying Canadian energy and natural resource firms?',
    'Protection of Canadian industries and real estate from foreign influence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (protÃ©ger les entreprises stratÃ©giques ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government prevent foreign companies from buying Canadian energy and natural resource firms?' 
        AND d.is_deleted = FALSE
  );
-- 13. (suite) Regulating foreign-owned media
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada introduce stricter regulations on foreign-owned media companies operating in Canada?',
    'Protection of Canadian industries and real estate from foreign influence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (rÃ©guler davantage les mÃ©dias Ã©trangers ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada introduce stricter regulations on foreign-owned media companies operating in Canada?' 
        AND d.is_deleted = FALSE
  );
-- 14. Social Policies & Ethics
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should euthanasia (Medical Assistance in Dying) be expanded to include individuals with severe mental illnesses?',
    'Controversial social issues affecting public policy.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (Ã©tendre l'aide mÃ©dicale Ã  mourir ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should euthanasia (Medical Assistance in Dying) be expanded to include individuals with severe mental illnesses?' 
        AND d.is_deleted = FALSE
  );
-- 14. (suite) Right to Disconnect law
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada make it illegal for employers to contact employees outside working hours (Right to Disconnect law)?',
    'Controversial social issues affecting public policy.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Employment & Labor Rights'
  AND fmt.name = 'binary'    -- oui/non (instituer un droit Ã  la dÃ©connexion ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada make it illegal for employers to contact employees outside working hours (Right to Disconnect law)?' 
        AND d.is_deleted = FALSE
  );
-- 14. (suite) Extended parental leave
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should parental leave be extended to 24 months with full pay?',
    'Controversial social issues affecting public policy.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Employment & Labor Rights'
  AND fmt.name = 'binary'    -- oui/non (allonger le congÃ© parental payÃ© ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should parental leave be extended to 24 months with full pay?' 
        AND d.is_deleted = FALSE
  );
-- 14. (suite) **[Removed duplicate debate on drug decriminalization]**
-- 15. National Security & Border Control
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada introduce stronger border controls to limit illegal immigration?',
    'Immigration, refugee policies, and law enforcement.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (renforcer le contrÃ´le aux frontiÃ¨res ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada introduce stronger border controls to limit illegal immigration?' 
        AND d.is_deleted = FALSE
  );
-- 15. (suite) Ban dual citizenship
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada ban dual citizenship to prevent foreign influence in domestic affairs?',
    'Immigration, refugee policies, and law enforcement.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (interdire la double citoyennetÃ© ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada ban dual citizenship to prevent foreign influence in domestic affairs?' 
        AND d.is_deleted = FALSE
  );
-- 15. (suite) Intelligence surveillance vs civil rights
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada increase intelligence surveillance on individuals suspected of extremist activity, even without criminal evidence?',
    'Immigration, refugee policies, and law enforcement.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Crime & Policing'
  AND fmt.name = 'binary'    -- oui/non (surveillance accrue sans preuve ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada increase intelligence surveillance on individuals suspected of extremist activity, even without criminal evidence?' 
        AND d.is_deleted = FALSE
  );
-- 16. Indigenous Reconciliation
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada legally require companies to obtain Indigenous approval before resource projects on Indigenous land?',
    'Addressing past injustices and Indigenous governance.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND fmt.name = 'scale_5'    -- 3 options (oui veto, non mais consultation, non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada legally require companies to obtain Indigenous approval before resource projects on Indigenous land?' 
        AND d.is_deleted = FALSE
  );
-- 16. (suite) National Indigenous holiday
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada implement a national holiday for recognizing Indigenous history and culture?',
    'Addressing past injustices and Indigenous governance.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND fmt.name = 'binary'    -- oui/non (crÃ©er un jour fÃ©riÃ© autochtone ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada implement a national holiday for recognizing Indigenous history and culture?' 
        AND d.is_deleted = FALSE
  );
-- 16. (suite) Full Indigenous sovereignty
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Indigenous communities have full sovereignty over their governance, separate from federal/provincial laws?',
    'Addressing past injustices and Indigenous governance.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND fmt.name = 'scale_5'    -- 3 options (pleine souverainetÃ©, autonomie accrue, statu quo)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Indigenous communities have full sovereignty over their governance, separate from federal/provincial laws?' 
        AND d.is_deleted = FALSE
  );
-- 17. Media, Culture & National Identity
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada impose a minimum percentage of Canadian content on streaming platforms (e.g., Netflix, Disney+)?',
    'Strengthening Canadian culture and media presence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (imposer un quota de contenu canadien ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada impose a minimum percentage of Canadian content on streaming platforms (e.g., Netflix, Disney+)?' 
        AND d.is_deleted = FALSE
  );
-- 17. (suite) Mandatory Canadian history in curriculum
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canadian history, including past government injustices, be mandatory in high school education?',
    'Strengthening Canadian culture and media presence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (rendre obligatoire ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canadian history, including past government injustices, be mandatory in high school education?' 
        AND d.is_deleted = FALSE
  );
-- 17. (suite) Ban foreign funding of political advocacy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada ban foreign governments from funding political advocacy campaigns within the country?',
    'Strengthening Canadian culture and media presence.',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (interdire le financement Ã©tranger de campagnes politiques ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada ban foreign governments from funding political advocacy campaigns within the country?' 
        AND d.is_deleted = FALSE
  );
-- (Questions additionnelles basÃ©es sur lâ€™actualitÃ© du 20 janvier 2025)
-- 18. Climate Change and Environmental Policies
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada implement a national strategy to address the increasing frequency and severity of natural disasters attributed to climate change?',
    'Climate Change and Environmental Policies',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Environment & Climate Change'
  AND fmt.name = 'binary'    -- oui/non (mettre en place une stratÃ©gie nationale ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada implement a national strategy to address the increasing frequency and severity of natural disasters attributed to climate change?' 
        AND d.is_deleted = FALSE
  );
-- 18. (suite) Funding climate resilience research
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government increase funding for research and initiatives aimed at mitigating the impacts of climate change, given the record C$8.5 billion in insured losses from 2024 weather events?',
    'Climate Change and Environmental Policies',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Environment & Climate Change'
  AND fmt.name = 'binary'    -- oui/non (augmenter les financements ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government increase funding for research and initiatives aimed at mitigating the impacts of climate change, given the record C$8.5 billion in insured losses from 2024 weather events?' 
        AND d.is_deleted = FALSE
  );
-- 19. Political Leadership and Governance
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'In light of Prime Minister Justin Trudeau\'s resignation, should Canada hold an early federal election to select new leadership?',
    'Political Leadership and Governance',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND fmt.name = 'binary'    -- oui/non (dÃ©clencher des Ã©lections anticipÃ©es ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'In light of Prime Minister Justin Trudeau''s resignation, should Canada hold an early federal election to select new leadership?' 
        AND d.is_deleted = FALSE
  );
-- 19. (suite) Transparency in leadership transitions
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government introduce policies to ensure greater transparency and accountability in leadership transitions?',
    'Political Leadership and Governance',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND fmt.name = 'binary'    -- oui/non (introduire de nouvelles mesures de transparence ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government introduce policies to ensure greater transparency and accountability in leadership transitions?' 
        AND d.is_deleted = FALSE
  );
-- 20. Immigration and Population Growth
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Given the recent reduction in immigration targets due to challenges in housing and social services, should Canada further adjust its immigration policies?',
    'Immigration and Population Growth',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (ajuster davantage les cibles dâ€™immigration ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Given the recent reduction in immigration targets due to challenges in housing and social services, should Canada further adjust its immigration policies?' 
        AND d.is_deleted = FALSE
  );
-- 20. (suite) Regulate international student admissions
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government implement stricter regulations on international student admissions to prevent exploitation and ensure adequate resources?',
    'Immigration and Population Growth',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (durcir les rÃ¨gles pour les Ã©tudiants internationaux ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government implement stricter regulations on international student admissions to prevent exploitation and ensure adequate resources?' 
        AND d.is_deleted = FALSE
  );
-- 21. Indigenous Rights and Reconciliation
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Considering funding challenges for research on residential schools, should Canada increase financial support for Indigenous-led initiatives to locate missing children and unmarked graves?',
    'Indigenous Rights and Reconciliation',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND fmt.name = 'binary'    -- oui/non (accroÃ®tre le financement ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Considering funding challenges for research on residential schools, should Canada increase financial support for Indigenous-led initiatives to locate missing children and unmarked graves?' 
        AND d.is_deleted = FALSE
  );
-- 21. (suite) Criminalize residential school denialism
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the denial of atrocities linked to residential schools be criminalized to combat misinformation and promote reconciliation?',
    'Indigenous Rights and Reconciliation',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND fmt.name = 'binary'    -- oui/non (criminaliser le nÃ©gationnisme ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the denial of atrocities linked to residential schools be criminalized to combat misinformation and promote reconciliation?' 
        AND d.is_deleted = FALSE
  );
-- 22. Media and Information Access
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada amend the Online News Act to address the unintended consequences of news content being blocked on social media platforms?',
    'Media and Information Access',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (amender la loi sur les actualitÃ©s en ligne ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada amend the Online News Act to address the unintended consequences of news content being blocked on social media platforms?' 
        AND d.is_deleted = FALSE
  );
-- 22. (suite) Support for local news organizations
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government provide support to local news organizations affected by decreased online visibility due to platform restrictions?',
    'Media and Information Access',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Media, Culture & National Identity'
  AND fmt.name = 'binary'    -- oui/non (soutenir financiÃ¨rement les mÃ©dias locaux affectÃ©s ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government provide support to local news organizations affected by decreased online visibility due to platform restrictions?' 
        AND d.is_deleted = FALSE
  );
-- 23. Immigration and Social Integration
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'In light of the recent backlash against immigrants, should Canada implement additional programs to promote social integration and combat xenophobia?',
    'Immigration and Social Integration',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (lancer des programmes dâ€™intÃ©gration supplÃ©mentaires ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'In light of the recent backlash against immigrants, should Canada implement additional programs to promote social integration and combat xenophobia?' 
        AND d.is_deleted = FALSE
  );
-- 23. (suite) Reassess immigration policies (housing/cost concerns)
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government reassess its immigration policies to balance economic needs with public concerns about housing and cost of living?',
    'Immigration and Social Integration',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Immigration & Refugee Policy'
  AND fmt.name = 'binary'    -- oui/non (rÃ©Ã©valuer la politique dâ€™immigration ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government reassess its immigration policies to balance economic needs with public concerns about housing and cost of living?' 
        AND d.is_deleted = FALSE
  );
-- 24. Defense and Military Spending
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Given criticisms about Canada\'s defense spending, should the government expedite plans to meet NATO\'s target of allocating 2% of GDP to defense by 2032?',
    'Defense and Military Spending',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (accÃ©lÃ©rer l\'atteinte de 2% du PIB en dÃ©fense ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Given criticisms about Canada''s defense spending, should the government expedite plans to meet NATO''s target of allocating 2% of GDP to defense by 2032?' 
        AND d.is_deleted = FALSE
  );
-- 24. (suite) Prioritize specific defense investments
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should Canada prioritize investments in specific areas of defense, such as cybersecurity or Arctic sovereignty, in response to evolving global threats?',
    'Defense and Military Spending',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Foreign Policy & National Security'
  AND fmt.name = 'binary'    -- oui/non (prioriser la cybersÃ©curitÃ©/Arctique ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should Canada prioritize investments in specific areas of defense, such as cybersecurity or Arctic sovereignty, in response to evolving global threats?' 
        AND d.is_deleted = FALSE
  );
-- 25. Public Health and Drug Policy
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'With provinces seeking to expand involuntary treatment for drug users, should Canada establish a national framework to regulate such practices?',
    'Public Health and Drug Policy',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (Ã©tablir un cadre national ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'With provinces seeking to expand involuntary treatment for drug users, should Canada establish a national framework to regulate such practices?' 
        AND d.is_deleted = FALSE
  );
-- 25. (suite) Funding voluntary addiction treatment
INSERT INTO home_debatetopic (debatecategory_id, responseformat_id, title, description, created_by_id, created_at, updated_at, is_deleted, deleted_at)
SELECT 
    cat.id, fmt.id,
    'Should the government increase funding for voluntary addiction treatment programs and mental health services as an alternative to involuntary treatment?',
    'Public Health and Drug Policy',
    usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory cat, home_responseformat fmt, core_customuser usr
WHERE cat.name = 'Healthcare & Public Health'
  AND fmt.name = 'binary'    -- oui/non (financer davantage les services volontaires ou non)
  AND usr.username = 'KingKlown'
  AND NOT EXISTS (
      SELECT 1 FROM home_debatetopic d 
      WHERE d.title = 'Should the government increase funding for voluntary addiction treatment programs and mental health services as an alternative to involuntary treatment?' 
        AND d.is_deleted = FALSE
  );
