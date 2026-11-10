
-- German Energy Data Platform
-- Raw electricity generation observations

CREATE TABLE IF NOT EXISTS raw.electricity_generation (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    interval_start TIMESTAMP NOT NULL,
    interval_end TIMESTAMP NOT NULL,

    energy_source VARCHAR(100) NOT NULL,
    generation_mwh NUMERIC(18, 2),

    source_file VARCHAR(255) NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_generation_interval
        CHECK (interval_end > interval_start),

    CONSTRAINT chk_generation_nonnegative
        CHECK (generation_mwh >= 0),

    CONSTRAINT uq_generation_observation
        UNIQUE (interval_start, interval_end, energy_source)
);
