
-- German Energy Data Platform
-- Daily renewable electricity generation share

CREATE OR REPLACE VIEW marts.daily_renewable_share AS

SELECT
    generation_date,

    SUM(total_generation_mwh)
        AS total_generation_mwh,

    SUM(total_generation_mwh)
        FILTER (WHERE is_renewable)
        AS renewable_generation_mwh,

    SUM(total_generation_mwh)
        FILTER (WHERE NOT is_renewable)
        AS non_renewable_generation_mwh,

    ROUND(
        100.0 *
        SUM(total_generation_mwh)
            FILTER (WHERE is_renewable)
        / NULLIF(SUM(total_generation_mwh), 0),
        2
    ) AS renewable_share_pct,

    SUM(missing_observations)
        AS missing_observations

FROM marts.daily_generation_by_source

GROUP BY generation_date;
