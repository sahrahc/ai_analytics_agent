"""Metric: roasReasoning: ROAS is defined as the ratio of total revenue to total cost at the grain of fct_campaign_daily (daily summary of ad campaign performance). At this grain we must aggregate revenue and cost across the selected grouping (here we aggregate by campaign_key and date_key to preserve the table grain) and compute the ratio as SUM(revenue_usd) / NULLIF(SUM(cost_usd), 0) to avoid divide-by-zero. The metric metadata specifies numerator= revenue_usd and denominator= cost_usd, so the SQL sums those expressions from the specified model.Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']Columns Used: ['campaign_key', 'date_key', 'revenue_usd', 'cost_usd']Warnings: ['The semantic model provided for fct_campaign_daily lists only campaign_key and date_key columns. revenue_usd and cost_usd are not present in the provided metadata for fct_campaign_daily. Confirm these columns exist in the actual table or adjust the metric definition/source table accordingly.', 'ROAS division handles zero cost by returning NULL when total cost is zero (NULLIF/CASE used).']"""

SELECT
  campaign_key,
  date_key,
  SUM(revenue_usd) AS revenue_usd,
  SUM(cost_usd) AS cost_usd,
  CASE WHEN SUM(cost_usd) = 0 THEN NULL ELSE SUM(revenue_usd) / SUM(cost_usd) END AS roas
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily
GROUP BY campaign_key, date_key;"""Metric: roas
Reasoning: Metric 'roas' is defined on model fct_campaign_daily as a ratio of numerator revenue_usd and denominator cost_usd. The fct_campaign_daily model in the provided semantic metadata contains campaign_key and date_key columns but does not list revenue_usd or cost_usd. Respecting the metric definition and table grain (daily per campaign), the SQL below computes the sum of revenue and cost at the campaign_key, date_key grain and calculates the ratio, protecting against division by zero. Note: revenue_usd and cost_usd are referenced as if they exist on fct_campaign_daily; metadata does not include these columns, so the query will fail unless those columns are actually present or a different source with those fields is provided.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']
Columns Used: ['campaign_key', 'date_key', 'revenue_usd', 'cost_usd']
Warnings: ['The semantic metadata for fct_campaign_daily does not list columns revenue_usd or cost_usd. The metric definition references them; confirm these columns exist or provide the correct source/model that contains revenue_usd and cost_usd.', 'Aggregation is applied at the table grain (campaign_key, date_key). If a different grain or additional dimension filters are required, adjust GROUP BY accordingly.']
"""

SELECT
  campaign_key,
  date_key,
  SUM(revenue_usd) AS revenue_usd,
  SUM(cost_usd) AS cost_usd,
  CASE WHEN SUM(cost_usd) = 0 THEN NULL ELSE SUM(revenue_usd) / SUM(cost_usd) END AS roas
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily
GROUP BY campaign_key, date_key;"""Metric: roas
Reasoning: roas is a ratio metric defined as revenue_usd / cost_usd at the fct_campaign_daily model grain (daily campaign-level). The source model fct_campaign_daily is a daily summary of campaign performance (campaign_key, date_key). To compute ROAS reliably we must aggregate revenue and cost (SUM) at the model grain and then divide, protecting against division by zero with NULLIF. The semantic metadata for fct_campaign_daily does not list revenue_usd or cost_usd, so the SQL below assumes those columns exist in STREAMING_ADS.streaming_ads_schema.fct_campaign_daily. If those columns live in a different model or under different names, the query must be adjusted.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']
Columns Used: ['campaign_key', 'date_key', 'revenue_usd', 'cost_usd']
Warnings: ['The semantic model for fct_campaign_daily only lists campaign_key and date_key. revenue_usd and cost_usd are not present in the provided metadata. The SQL assumes revenue_usd and cost_usd exist in STREAMING_ADS.streaming_ads_schema.fct_campaign_daily — adjust column names or source model if they are located elsewhere.', 'ROAS is computed as SUM(revenue_usd) / SUM(cost_usd) and will return NULL when the summed cost is zero to avoid division-by-zero errors.']
"""

SELECT
  campaign_key,
  date_key,
  SUM(revenue_usd) AS revenue_usd,
  SUM(cost_usd) AS cost_usd,
  CASE WHEN SUM(cost_usd) = 0 THEN NULL ELSE SUM(revenue_usd) / NULLIF(SUM(cost_usd), 0) END AS roas
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily
GROUP BY campaign_key, date_key;"""Metric: roas
Reasoning: The metric is defined as a ratio with numerator = revenue_usd and denominator = cost_usd on the fct_campaign_daily model. The fct_campaign_daily table is already at the daily campaign grain (campaign_key, date_key). Do not invent joins. Compute ROAS per row using revenue_usd / cost_usd and protect against zero or NULL cost to avoid division errors. Return campaign_key and date_key to preserve table grain and make the metric sliceable by those dimensions.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']
Columns Used: ['campaign_key', 'date_key', 'revenue_usd', 'cost_usd']
Warnings: ['If cost_usd is zero or NULL, ROAS is returned as NULL to avoid division by zero.', 'The fct_campaign_daily model already contains a precomputed roas column; this query computes ROAS from the defined numerator and denominator (revenue_usd / cost_usd) to respect the metric definition.', 'This query preserves the table grain (campaign_key, date_key). If you need aggregated ROAS across campaigns or dates, apply aggregation for numerator and denominator first (SUM(revenue_usd) / SUM(cost_usd)) with the same zero-check.']
"""

SELECT
  campaign_key,
  date_key,
  revenue_usd,
  cost_usd,
  CASE
    WHEN cost_usd IS NULL OR cost_usd = 0 THEN NULL
    ELSE revenue_usd / cost_usd
  END AS roas
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily;"""Analysis Request: Find historical roas by week
Reasoning: We have a roas metric stored on fct_campaign_daily (column roas) and revenue_usd / cost_usd columns on the same table. To compute historical ROAS by calendar week we should aggregate daily rows to weekly level using the dim_calendar relationship (fct_campaign_daily.date_key -> dim_calendar.date_key). To avoid averaging per-day ROAS (which is biased), compute weekly ROAS as sum(revenue_usd) / sum(cost_usd). Handle zero cost with NULLIF to avoid division-by-zero. Return year and week from dim_calendar and order chronologically.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily', 'STREAMING_ADS.streaming_ads_schema.dim_calendar']
Columns Used: ['fct_campaign_daily.date_key', 'fct_campaign_daily.revenue_usd', 'fct_campaign_daily.cost_usd', 'dim_calendar.date_key', 'dim_calendar.year', 'dim_calendar.week']
Warnings: ['Weeks spanning year boundaries are grouped by the year value in dim_calendar. If you want ISO-week semantics or a different week definition, confirm dim_calendar.week semantics.', 'Rows with SUM(cost_usd) = 0 will yield NULL for roas_weekly to avoid division by zero.']
"""

SELECT
  c.year AS year,
  c.week AS week,
  SUM(f.revenue_usd) AS revenue_usd_weekly,
  SUM(f.cost_usd) AS cost_usd_weekly,
  CASE
    WHEN SUM(f.cost_usd) = 0 THEN NULL
    ELSE SUM(f.revenue_usd) / NULLIF(SUM(f.cost_usd), 0)
  END AS roas_weekly
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily f
JOIN STREAMING_ADS.streaming_ads_schema.dim_calendar c
  ON f.date_key = c.date_key
GROUP BY
  c.year,
  c.week
ORDER BY
  c.year,
  c.week;