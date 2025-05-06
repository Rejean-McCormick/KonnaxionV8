-- --------------------------------------------------
-- Section: Bases de données
-- --------------------------------------------------
DROP DATABASE IF EXISTS konnaxion_db;
DROP DATABASE IF EXISTS pulse_db;
CREATE DATABASE konnaxion_db;
CREATE DATABASE pulse_db;
\connect konnaxion_db;

-- --------------------------------------------------
-- Section: Extensions PostgreSQL requises
-- --------------------------------------------------
--CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Application Konnaxion - Core
CREATE TABLE core_customuser (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    language_preference VARCHAR(10) NOT NULL DEFAULT 'en',
    device_details JSONB,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    offline_sync_token VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE core_systemconfiguration (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE core_configurationchangelog (
    id BIGSERIAL PRIMARY KEY,
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    change_reason TEXT,
    changed_by_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    configuration_id BIGINT NOT NULL REFERENCES core_systemconfiguration(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnaxion - Search
CREATE TABLE search_searchquerylog (
    id BIGSERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    results_count INTEGER NOT NULL DEFAULT 0,
    user_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE search_searchindex (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    settings JSONB NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnaxion - Ai
CREATE TABLE ai_airesult (
    id BIGSERIAL PRIMARY KEY,
    input_data JSONB NOT NULL,
    result_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnaxion - Notifications
CREATE TABLE notifications_notification (
    id BIGSERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    read BOOLEAN NOT NULL DEFAULT FALSE,
    notification_type VARCHAR(50) NOT NULL DEFAULT 'info',
    recipient_id BIGINT REFERENCES core_customuser(id) ON DELETE CASCADE,
    sender_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnaxion - Messaging
CREATE TABLE messaging_conversation (
    id BIGSERIAL PRIMARY KEY,
    topic VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE messaging_message (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    sender_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    conversation_id BIGINT NOT NULL REFERENCES messaging_conversation(id) ON DELETE CASCADE,
    is_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnaxion - Ekoh
CREATE TABLE ekoh_expertisetag (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE ekoh_reputationprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES core_customuser(id) ON DELETE CASCADE,
    reputation_score INTEGER NOT NULL DEFAULT 0,
    ethical_multiplier DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE ekoh_reputationevent (
    id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT NOT NULL REFERENCES ekoh_reputationprofile(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    impact INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE ekoh_weightedvote (
    id BIGSERIAL PRIMARY KEY,
    debate_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    weight DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Foundation
CREATE TABLE foundation_knowledgeunit (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Konnectedcommunity
CREATE TABLE konnectedcommunity_discussionthread (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE konnectedcommunity_comment (
    id BIGSERIAL PRIMARY KEY,
    thread_id BIGINT NOT NULL REFERENCES konnectedcommunity_discussionthread(id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    parent_id BIGINT REFERENCES konnectedcommunity_comment(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Learning
CREATE TABLE learning_question (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL DEFAULT 'text',
    lesson_id BIGINT,
    created_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE learning_answer (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL REFERENCES learning_question(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    respondent_id BIGINT REFERENCES core_customuser(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE learning_lesson (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_by_id BIGINT REFERENCES core_customuser(id) ON DELETE CASCADE,
    knowledge_unit_id BIGINT REFERENCES foundation_knowledgeunit(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE learning_quiz (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    knowledge_unit_id BIGINT REFERENCES foundation_knowledgeunit(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Offline
CREATE TABLE offline_offlinecontentpackage (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Paths
CREATE TABLE paths_learningpath (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE paths_pathstep (
    id BIGSERIAL PRIMARY KEY,
    learning_path_id BIGINT NOT NULL REFERENCES paths_learningpath(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Konnected - Team
CREATE TABLE team_team (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE team_teaminvitation (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL REFERENCES team_team(id) ON DELETE CASCADE,
    invited_user_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    accepted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Projects
CREATE TABLE projects_project (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'planning',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE projects_milestone (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES projects_project(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    due_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE projects_task (
    id BIGSERIAL PRIMARY KEY,
    milestone_id BIGINT REFERENCES projects_milestone(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Gap Analysis
CREATE TABLE gap_analysis_gapanalysis (
    id BIGSERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    description TEXT,
    created_by_id BIGINT REFERENCES core_customuser(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Expert Match
CREATE TABLE expert_match_candidateprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    expertise_area VARCHAR(255) NOT NULL,
    experience_years INTEGER NOT NULL DEFAULT 0,
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE expert_match_expertmatchrequest (
    id BIGSERIAL PRIMARY KEY,
    requester_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE SET NULL,
    expertise_needed VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE expert_match_matchscore (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES expert_match_expertmatchrequest(id) ON DELETE CASCADE,
    candidate_id BIGINT NOT NULL REFERENCES expert_match_candidateprofile(id) ON DELETE CASCADE,
    score DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Team Formation
CREATE TABLE team_formation_teamformationrequest (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects_project(id) ON DELETE SET NULL,
    requested_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE SET NULL,
    team_size INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE team_formation_teamformationcandidate (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES team_formation_teamformationrequest(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    suitability_score DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Collab Spaces
CREATE TABLE collab_spaces_collabspace (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE collab_spaces_chatmessage (
    id BIGSERIAL PRIMARY KEY,
    space_id BIGINT NOT NULL REFERENCES collab_spaces_collabspace(id) ON DELETE CASCADE,
    sender_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE collab_spaces_document (
    id BIGSERIAL PRIMARY KEY,
    space_id BIGINT NOT NULL REFERENCES collab_spaces_collabspace(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Keenkonnect - Knowledge Hub
CREATE TABLE knowledge_hub_knowledgedocument (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    author_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    version VARCHAR(50) NOT NULL DEFAULT '1.0',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE knowledge_hub_documentrevision (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES knowledge_hub_knowledgedocument(id) ON DELETE CASCADE,
    revised_by_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    changes TEXT,
    version_label VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Ethikos - Home
CREATE TABLE home_debatetopic (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE home_featureddebate (
    id BIGSERIAL PRIMARY KEY,
    debate_title VARCHAR(255) NOT NULL,
    summary TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE home_personalizedrecommendation (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    recommended_debate VARCHAR(255) NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Ethikos - Debate Arena
CREATE TABLE debate_arena_debatesession (
    id BIGSERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    description TEXT,
    moderator_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE debate_arena_argument (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    debate_session_id BIGINT NOT NULL REFERENCES debate_arena_debatesession(id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    parent_id BIGINT REFERENCES debate_arena_argument(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE debate_arena_voterecord (
    id BIGSERIAL PRIMARY KEY,
    debate_session_id BIGINT NOT NULL REFERENCES debate_arena_debatesession(id) ON DELETE CASCADE,
    argument_id BIGINT NOT NULL REFERENCES debate_arena_argument(id) ON DELETE CASCADE,
    voter_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    vote_value INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Ethikos - Stats
CREATE TABLE stats_debatestatistic (
    id BIGSERIAL PRIMARY KEY,
    debate_session_id BIGINT NOT NULL REFERENCES debate_arena_debatesession(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE stats_debateeventlog (
    id BIGSERIAL PRIMARY KEY,
    debate_session_id BIGINT NOT NULL REFERENCES debate_arena_debatesession(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    description TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Application Ethikos - Knowledge Base
CREATE TABLE knowledge_base_debatearchive (
    id BIGSERIAL PRIMARY KEY,
    debate_title VARCHAR(255) NOT NULL,
    transcript TEXT,
    archive_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Ethikos - Prioritization
CREATE TABLE prioritization_debateprioritization (
    id BIGSERIAL PRIMARY KEY,
    debate_topic VARCHAR(255) NOT NULL,
    priority_level INTEGER NOT NULL,
    rationale TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Ethikos - Resolution
CREATE TABLE resolution_debateresolution (
    id BIGSERIAL PRIMARY KEY,
    debate_session_id BIGINT NOT NULL UNIQUE REFERENCES debate_arena_debatesession(id) ON DELETE CASCADE,
    resolution_text TEXT NOT NULL,
    approved_by_id BIGINT REFERENCES core_customuser(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Kreative - Artworks
CREATE TABLE artworks_exhibition (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE artworks_artwork (
    id BIGSERIAL PRIMARY KEY,
    exhibition_id BIGINT REFERENCES artworks_exhibition(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    creator_name VARCHAR(255),
    image VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Kreative - Marketplace
CREATE TABLE marketplace_artistprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES core_customuser(id) ON DELETE CASCADE,
    display_name VARCHAR(255) NOT NULL,
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE marketplace_marketplacelisting (
    id BIGSERIAL PRIMARY KEY,
    artist_profile_id BIGINT NOT NULL REFERENCES marketplace_artistprofile(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE marketplace_commission (
    id BIGSERIAL PRIMARY KEY,
    listing_id BIGINT NOT NULL REFERENCES marketplace_marketplacelisting(id) ON DELETE CASCADE,
    requested_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    details TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'requested',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Kreative - Kreativecommunity
CREATE TABLE kreativecommunity_artworkreview (
    id BIGSERIAL PRIMARY KEY,
    artwork_id BIGINT NOT NULL REFERENCES artworks_artwork(id) ON DELETE CASCADE,
    reviewed_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    review_text TEXT,
    rating INTEGER,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE kreativecommunity_communitypost (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    posted_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE kreativecommunity_postcomment (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES kreativecommunity_communitypost(id) ON DELETE CASCADE,
    commented_by_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    parent_comment_id BIGINT REFERENCES kreativecommunity_postcomment(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Application Kreative - Immersive
CREATE TABLE immersive_immersiveexperience (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    media_url VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- --------------------------------------------------
-- Tables intermédiaires pour relations Many-to-Many
-- --------------------------------------------------
CREATE TABLE team_team_members (
    team_id BIGINT NOT NULL REFERENCES team_team(id) ON DELETE CASCADE,
    customuser_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    PRIMARY KEY (team_id, customuser_id)
);

CREATE TABLE messaging_conversation_participants (
    conversation_id BIGINT NOT NULL REFERENCES messaging_conversation(id) ON DELETE CASCADE,
    customuser_id BIGINT NOT NULL REFERENCES core_customuser(id) ON DELETE CASCADE,
    PRIMARY KEY (conversation_id, customuser_id)
);

CREATE TABLE ekoh_reputationprofile_expertise_tags (
    reputationprofile_id BIGINT NOT NULL REFERENCES ekoh_reputationprofile(id) ON DELETE CASCADE,
    expertisetag_id BIGINT NOT NULL REFERENCES ekoh_expertisetag(id) ON DELETE CASCADE,
    PRIMARY KEY (reputationprofile_id, expertisetag_id)
);

-- --------------------------------------------------
-- Conversion des tables en Hypertables TimescaleDB
-- --------------------------------------------------
--SELECT create_hypertable('stats_debatestatistic', 'recorded_at');
--SELECT create_hypertable('stats_debateeventlog', 'timestamp');

-- --------------------------------------------------
-- Indexation supplémentaire (ex: index trigram pour recherche textuelle)
-- --------------------------------------------------
CREATE INDEX idx_ekoh_expertisetag_name_trgm ON ekoh_expertisetag USING GIN (name gin_trgm_ops);
