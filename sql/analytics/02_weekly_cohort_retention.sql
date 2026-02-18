WITH enrolled AS (
  SELECT
    l.patient_id,
    date_trunc('week', l.enrolled_at)::date AS cohort_week,
    l.enrolled_at
  FROM fact_patient_lifecycle l
  WHERE l.enrolled_at IS NOT NULL
),
activity AS (
  SELECT
    e.patient_id,
    e.cohort_week,
    date_trunc('week', ev.event_ts)::date AS activity_week
  FROM enrolled e
  JOIN fact_patient_event ev
    ON ev.patient_id = e.patient_id
  WHERE ev.event_ts >= e.enrolled_at
),
week_indexed AS (
  SELECT
    cohort_week,
    patient_id,
    ((activity_week - cohort_week) / 7) AS week_n
  FROM activity
)
SELECT
  cohort_week,
  week_n,
  COUNT(DISTINCT patient_id) AS active_patients,
  ROUND(
    COUNT(DISTINCT patient_id)::numeric
    / NULLIF((SELECT COUNT(*) FROM enrolled e2 WHERE e2.cohort_week = week_indexed.cohort_week), 0),
    3
  ) AS retention_rate
FROM week_indexed
WHERE week_n BETWEEN 0 AND 12
GROUP BY 1, 2
ORDER BY cohort_week, week_n;

