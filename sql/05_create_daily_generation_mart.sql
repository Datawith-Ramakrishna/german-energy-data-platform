
-- German Energy Data Platform
-- Daily electricity generation by energy source

CREATE OR REPLACE VIEW marts.daily_generation_by_source AS
SELECT
    generation_date,
    energy_source,
    is_renewable,

    SUM(generation_mwh) AS total_generation_mwh,

    COUNT(*) AS hourly_observations,

    COUNT(generation_mwh) AS valid_observations,

    COUNT(*) - COUNT(generation_mwh)
        AS missing_observations

FROM staging.stg_electricity_generation

GROUP BY
    generation_date,
    energy_source,
    is_renewable;
