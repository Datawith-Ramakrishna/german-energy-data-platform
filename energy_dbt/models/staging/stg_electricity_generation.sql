
{{ config(materialized='view') }}

WITH source_data AS (

    SELECT *
    FROM {{ source('energy_raw', 'electricity_generation') }}

),

renamed AS (

    SELECT
        id AS generation_id,
        interval_start,
        interval_end,

        interval_start::DATE AS generation_date,

        EXTRACT(HOUR FROM interval_start)::INTEGER
            AS generation_hour,

        LOWER(REPLACE(energy_source, ' ', '_'))
            AS energy_source,

        generation_mwh,

        CASE
            WHEN energy_source IN (
                'Biomass',
                'Hydropower',
                'Wind offshore',
                'Wind onshore',
                'Photovoltaics',
                'Other renewable'
            )
            THEN TRUE
            ELSE FALSE
        END AS is_renewable,

        source_file,
        ingested_at

    FROM source_data

)

SELECT *
FROM renamed
