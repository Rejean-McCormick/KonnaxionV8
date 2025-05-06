-- dbethikos3.sql
-- 1) U.S. Tariffs & Canada’s Response
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada negotiate sector-based exemptions from U.S. tariffs rather than retaliating with tariffs on U.S. goods?',
  'U.S. plans a 25% tariff on Canadian imports; Canada is considering retaliation.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Economy & Taxation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada negotiate sector-based exemptions from U.S. tariffs rather than retaliating with tariffs on U.S. goods?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'If the U.S. proceeds with a 25% tariff on all Canadian imports, which approach should Canada prioritize?',
  'U.S. imposes broad tariffs on Canada – possible response strategies for Canada.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Economy & Taxation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'If the U.S. proceeds with a 25% tariff on all Canadian imports, which approach should Canada prioritize?'
      AND d.is_deleted = FALSE
  );

-- 2) Electoral System & Democracy
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada move to a proportional representation voting system to better reflect diverse political views?',
  'Upcoming federal elections and potential changes to the voting system.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada move to a proportional representation voting system to better reflect diverse political views?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada implement online voting in federal elections to increase accessibility?',
  'Upcoming federal elections and potential changes to the voting system.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada implement online voting in federal elections to increase accessibility?'
      AND d.is_deleted = FALSE
  );

-- 3) Environment & Energy Policy
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada stop approving new fossil fuel projects by 2030?',
  'Canada’s transition to a clean energy economy while balancing economic needs.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Environment & Climate Change'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada stop approving new fossil fuel projects by 2030?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'How should Canada finance the transition to a green economy?',
  'Canada’s transition to a clean energy economy while balancing economic needs.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Environment & Climate Change'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'How should Canada finance the transition to a green economy?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada ban single-use plastics completely within the next five years?',
  'Canada’s transition to a clean energy economy while balancing economic needs.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Environment & Climate Change'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada ban single-use plastics completely within the next five years?'
      AND d.is_deleted = FALSE
  );

-- 4) Food Safety & Public Health
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should food import regulations be strengthened to prevent contaminated products from entering Canada?',
  'Rise in salmonella cases due to contaminated food imports.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should food import regulations be strengthened to prevent contaminated products from entering Canada?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should companies responsible for foodborne illness outbreaks face increased financial penalties?',
  'Rise in salmonella cases due to contaminated food imports.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should companies responsible for foodborne illness outbreaks face increased financial penalties?'
      AND d.is_deleted = FALSE
  );

-- 5) Education & Youth Well-being
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should all public high schools be required to provide mental health education?',
  'Mental health programs in schools have been shown to reduce youth drug use.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should all public high schools be required to provide mental health education?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'How should the government address youth drug use prevention?',
  'Mental health programs in schools have been shown to reduce youth drug use.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'How should the government address youth drug use prevention?'
      AND d.is_deleted = FALSE
  );

-- 6) Housing Crisis & Affordability
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should Canada impose stricter regulations on foreign real estate investors to cool down the housing market?',
  'Rising housing costs and affordability issues in Canada’s major cities.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Housing & Urban Development'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should Canada impose stricter regulations on foreign real estate investors to cool down the housing market?'
      AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT
  cat.id, fmt.id,
  'Should the government invest more in public housing projects?',
  'Rising housing costs and affordability issues in Canada’s major cities.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Housing & Urban Development'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
    WHERE d.title = 'Should the government invest more in public housing projects?'
      AND d.is_deleted = FALSE
  );
