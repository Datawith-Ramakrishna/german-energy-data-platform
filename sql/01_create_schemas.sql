
-- German Energy Data Platform
-- Initialize PostgreSQL schemas

CREATE SCHEMA IF NOT EXISTS raw;

CREATE SCHEMA IF NOT EXISTS staging;

CREATE SCHEMA IF NOT EXISTS marts;

-- Verify schemas
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('raw', 'staging', 'marts')
ORDER BY schema_name;
