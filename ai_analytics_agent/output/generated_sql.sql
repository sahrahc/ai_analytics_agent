"""Analysis Request: Create a Snowflake SQL query that returns the daily campaign-level metrics from the fct_campaign_daily model.
Reasoning: The provided model fct_campaign_daily already contains daily, campaign-grain metrics. No additional joins or derived metrics were requested, so the query selects the relevant columns directly from the model's fully qualified name. The result is ordered by date_key and campaign_key to make downstream analysis easier.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']
Columns Used: ['campaign_key', 'date_key', 'impressions', 'clicks', 'conversions', 'click_through_conversions', 'view_through_conversions', 'revenue_usd', 'cost_usd', 'ctr', 'click_cvr', 'view_cvr', 'roas', 'loaded_at']
Warnings: ['No additional metric definitions were provided beyond the columns in the model; the query returns the stored metrics as-is.', 'date_key is of type text in metadata; if you need date arithmetic or ordering by calendar date, consider casting date_key to a DATE if it contains ISO date strings.']
"""

SELECT
  campaign_key,
  date_key,
  impressions,
  clicks,
  conversions,
  click_through_conversions,
  view_through_conversions,
  revenue_usd,
  cost_usd,
  ctr,
  click_cvr,
  view_cvr,
  roas,
  loaded_at
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily
ORDER BY date_key, campaign_key;"""Analysis Request: Aggregate campaign daily metrics by campaign_key and date, computing CTR, click CVR, and ROAS while handling divide-by-zero and casting the text date_key to a date.
Reasoning: The model fct_campaign_daily is a daily summary at the (campaign_key, date_key) grain. To avoid changing grain, aggregate by campaign_key and date_key. date_key is stored as text so convert to a date using TRY_TO_DATE to avoid errors on unexpected formats. Compute CTR, click CVR, and ROAS using summed numerators and NULLIF on denominators to prevent divide-by-zero. Use only columns present in the provided metadata and reference the fully-qualified table name in Snowflake.
Tables Used: ['STREAMING_ADS.streaming_ads_schema.fct_campaign_daily']
Columns Used: ['campaign_key', 'date_key', 'impressions', 'clicks', 'conversions', 'revenue_usd', 'cost_usd']
Warnings: ['date_key is stored as text; TRY_TO_DATE is used to coerce to a date. If date_key uses a non-standard format, some values may become NULL.', 'The table already contains precomputed metrics (ctr, click_cvr, roas). This query recomputes them from raw counts and amounts to ensure correctness at the aggregated level.', 'Division-by-zero is handled using NULLIF; results will be NULL where denominators sum to zero.']
"""

SELECT
  campaign_key,
  TRY_TO_DATE(date_key) AS date,
  SUM(impressions)       AS impressions,
  SUM(clicks)            AS clicks,
  SUM(conversions)       AS conversions,
  SUM(revenue_usd)       AS revenue_usd,
  SUM(cost_usd)          AS cost_usd,
  CASE WHEN SUM(impressions) = 0 THEN NULL ELSE SUM(clicks) / NULLIF(SUM(impressions), 0) END AS ctr,
  CASE WHEN SUM(clicks) = 0 THEN NULL ELSE SUM(conversions) / NULLIF(SUM(clicks), 0) END AS click_cvr,
  CASE WHEN SUM(cost_usd) = 0 THEN NULL ELSE SUM(revenue_usd) / NULLIF(SUM(cost_usd), 0) END AS roas
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily
GROUP BY
  campaign_key,
  TRY_TO_DATE(date_key)
ORDER BY
  date DESC,
  campaign_key;