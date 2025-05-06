-- 15. National Security & Border Control
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada introduce stronger border controls to limit illegal immigration?',
  'Immigration, refugee policies, and law enforcement.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Immigration & Refugee Policy'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada introduce stronger border controls to limit illegal immigration?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada ban dual citizenship to prevent foreign influence in domestic affairs?',
  'Immigration, refugee policies, and law enforcement.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Foreign Policy & National Security'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada ban dual citizenship to prevent foreign influence in domestic affairs?'
       AND d.is_deleted = FALSE
  );

-- 16. Indigenous Reconciliation
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada legally require companies to obtain Indigenous approval before resource projects on Indigenous land?',
  'Addressing past injustices and Indigenous governance.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada legally require companies to obtain Indigenous approval before resource projects on Indigenous land?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada implement a national holiday for recognizing Indigenous history and culture?',
  'Addressing past injustices and Indigenous governance.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada implement a national holiday for recognizing Indigenous history and culture?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Indigenous communities have full sovereignty over their governance, separate from federal/provincial laws?',
  'Addressing past injustices and Indigenous governance.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'scale_5'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Indigenous communities have full sovereignty over their governance, separate from federal/provincial laws?'
       AND d.is_deleted = FALSE
  );

-- 17. Media, Culture & National Identity
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada impose a minimum percentage of Canadian content on streaming platforms (e.g., Netflix, Disney+)?',
  'Strengthening Canadian culture and media presence.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Media, Culture & National Identity'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada impose a minimum percentage of Canadian content on streaming platforms (e.g., Netflix, Disney+)?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canadian history, including past government injustices, be mandatory in high school education?',
  'Strengthening Canadian culture and media presence.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Media, Culture & National Identity'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canadian history, including past government injustices, be mandatory in high school education?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada ban foreign governments from funding political advocacy campaigns within the country?',
  'Strengthening Canadian culture and media presence.',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Media, Culture & National Identity'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada ban foreign governments from funding political advocacy campaigns within the country?'
       AND d.is_deleted = FALSE
  );

-- 18. Climate Change and Environmental Policies
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada implement a national strategy to address the increasing frequency and severity of natural disasters attributed to climate change?',
  'Climate Change and Environmental Policies',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Environment & Climate Change'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada implement a national strategy to address the increasing frequency and severity of natural disasters attributed to climate change?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government increase funding for research and initiatives aimed at mitigating the impacts of climate change, given the record C$8.5 billion in insured losses from 2024 weather events?',
  'Climate Change and Environmental Policies',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Environment & Climate Change'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government increase funding for research and initiatives aimed at mitigating the impacts of climate change, given the record C$8.5 billion in insured losses from 2024 weather events?'
       AND d.is_deleted = FALSE
  );

-- 19. Political Leadership and Governance
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'In light of Prime Minister Justin Trudeau''s resignation, should Canada hold an early federal election to select new leadership?',
  'Political Leadership and Governance',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'In light of Prime Minister Justin Trudeau''s resignation, should Canada hold an early federal election to select new leadership?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government introduce policies to ensure greater transparency and accountability in leadership transitions?',
  'Political Leadership and Governance',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Governance, Democracy & Political Reform'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government introduce policies to ensure greater transparency and accountability in leadership transitions?'
       AND d.is_deleted = FALSE
  );

-- 20. Immigration and Population Growth
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Given the recent reduction in immigration targets due to challenges in housing and social services, should Canada further adjust its immigration policies?',
  'Immigration and Population Growth',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Immigration & Refugee Policy'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Given the recent reduction in immigration targets due to challenges in housing and social services, should Canada further adjust its immigration policies?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government implement stricter regulations on international student admissions to prevent exploitation and ensure adequate resources?',
  'Immigration and Population Growth',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Immigration & Refugee Policy'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government implement stricter regulations on international student admissions to prevent exploitation and ensure adequate resources?'
       AND d.is_deleted = FALSE
  );

-- 21. Indigenous Rights and Reconciliation (additional)
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Considering funding challenges for research on residential schools, should Canada increase financial support for Indigenous-led initiatives to locate missing children and unmarked graves?',
  'Indigenous Rights and Reconciliation',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Considering funding challenges for research on residential schools, should Canada increase financial support for Indigenous-led initiatives to locate missing children and unmarked graves?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the denial of atrocities linked to residential schools be criminalized to combat misinformation and promote reconciliation?',
  'Indigenous Rights and Reconciliation',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Indigenous Rights & Reconciliation'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the denial of atrocities linked to residential schools be criminalized to combat misinformation and promote reconciliation?'
       AND d.is_deleted = FALSE
  );

-- 22. Media and Information Access
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada amend the Online News Act to address the unintended consequences of news content being blocked on social media platforms?',
  'Media and Information Access',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Media, Culture & National Identity'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada amend the Online News Act to address the unintended consequences of news content being blocked on social media platforms?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government provide support to local news organizations affected by decreased online visibility due to platform restrictions?',
  'Media and Information Access',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Media, Culture & National Identity'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government provide support to local news organizations affected by decreased online visibility due to platform restrictions?'
       AND d.is_deleted = FALSE
  );

-- 23. Immigration and Social Integration
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'In light of the recent backlash against immigrants, should Canada implement additional programs to promote social integration and combat xenophobia?',
  'Immigration and Social Integration',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Immigration & Refugee Policy'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'In light of the recent backlash against immigrants, should Canada implement additional programs to promote social integration and combat xenophobia?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government reassess its immigration policies to balance economic needs with public concerns about housing and cost of living?',
  'Immigration and Social Integration',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Immigration & Refugee Policy'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government reassess its immigration policies to balance economic needs with public concerns about housing and cost of living?'
       AND d.is_deleted = FALSE
  );

-- 24. Defense and Military Spending
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Given criticisms about Canada''s defense spending, should the government expedite plans to meet NATO''s target of allocating 2% of GDP to defense by 2032?',
  'Defense and Military Spending',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Foreign Policy & National Security'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Given criticisms about Canada''s defense spending, should the government expedite plans to meet NATO''s target of allocating 2% of GDP to defense by 2032?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should Canada prioritize investments in specific areas of defense, such as cybersecurity or Arctic sovereignty, in response to evolving global threats?',
  'Defense and Military Spending',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Foreign Policy & National Security'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should Canada prioritize investments in specific areas of defense, such as cybersecurity or Arctic sovereignty, in response to evolving global threats?'
       AND d.is_deleted = FALSE
  );

-- 25. Public Health and Drug Policy
INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'With provinces seeking to expand involuntary treatment for drug users, should Canada establish a national framework to regulate such practices?',
  'Public Health and Drug Policy',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'With provinces seeking to expand involuntary treatment for drug users, should Canada establish a national framework to regulate such practices?'
       AND d.is_deleted = FALSE
  );

INSERT INTO home_debatetopic (
  debatecategory_id, responseformat_id, title, description,
  created_by_id, created_at, updated_at, is_deleted, deleted_at
)
SELECT cat.id, fmt.id,
  'Should the government increase funding for voluntary addiction treatment programs and mental health services as an alternative to involuntary treatment?',
  'Public Health and Drug Policy',
  usr.id, NOW(), NOW(), FALSE, NULL
FROM home_debatecategory AS cat
JOIN home_responseformat AS fmt ON fmt.name = 'binary'
JOIN core_customuser   AS usr ON usr.username = 'KingKlown'
WHERE cat.name = 'Healthcare & Public Health'
  AND NOT EXISTS (
    SELECT 1 FROM home_debatetopic d
     WHERE d.title = 'Should the government increase funding for voluntary addiction treatment programs and mental health services as an alternative to involuntary treatment?'
       AND d.is_deleted = FALSE
  );
