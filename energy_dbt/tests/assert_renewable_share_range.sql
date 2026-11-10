
SELECT
    generation_date,
    renewable_share_pct
FROM {{ ref('daily_renewable_share') }}
WHERE renewable_share_pct < 0
   OR renewable_share_pct > 100
   OR renewable_share_pct IS NULL
