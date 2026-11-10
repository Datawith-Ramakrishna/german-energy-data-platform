
-- German Energy Data Platform
-- Raw electricity generation data-quality checks

-- Check 1: Total records and missing values
SELECT
    COUNT(*) AS total_records,
    COUNT(*) FILTER (
        WHERE generation_mwh IS NULL
    ) AS missing_values
FROM raw.electricity_generation;


-- Check 2: Duplicate observations
-- Expected result: 0 rows
SELECT
    interval_start,
    interval_end,
    energy_source,
    COUNT(*) AS duplicate_count
FROM raw.electricity_generation
GROUP BY
    interval_start,
    interval_end,
    energy_source
HAVING COUNT(*) > 1;


-- Check 3: Invalid generation values
-- Expected result: 0
SELECT COUNT(*) AS negative_values
FROM raw.electricity_generation
WHERE generation_mwh < 0;


-- Check 4: Invalid hourly intervals
-- Expected result: 0
SELECT COUNT(*) AS invalid_intervals
FROM raw.electricity_generation
WHERE interval_end - interval_start
    <> INTERVAL '1 hour';


-- Check 5: Observations per energy source
-- Expected result: 744 rows per source
SELECT
    energy_source,
    COUNT(*) AS observations,
    COUNT(*) FILTER (
        WHERE generation_mwh IS NULL
    ) AS missing_values
FROM raw.electricity_generation
GROUP BY energy_source
ORDER BY energy_source;
