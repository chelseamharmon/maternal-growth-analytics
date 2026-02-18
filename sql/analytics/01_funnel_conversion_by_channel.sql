WITH base AS (
  SELECT
    ac.channel_name,
    l.patient_id,
    (l.lead_created_at IS NOT NULL)::int AS is_lead,
    (l.eligibility_verified_at IS NOT NULL)::int AS is_eligible,
    (l.intake_completed_at IS NOT NULL)::int AS is_intake,
    (l.enrolled_at IS NOT NULL)::int AS is_enrolled
  FROM fact_patient_lifecycle l
  JOIN dim_acquisition_channel ac
    ON ac.channel_id = l.channel_id
)
SELECT
  channel_name,
  COUNT(*) AS patients,
  SUM(is_lead) AS leads,
  SUM(is_eligible) AS eligible,
  SUM(is_intake) AS intake_completed,
  SUM(is_enrolled) AS enrolled,
  ROUND(SUM(is_eligible)::numeric / NULLIF(SUM(is_lead), 0), 3) AS lead_to_eligible_rate,
  ROUND(SUM(is_intake)::numeric / NULLIF(SUM(is_eligible), 0), 3) AS eligible_to_intake_rate,
  ROUND(SUM(is_enrolled)::numeric / NULLIF(SUM(is_intake), 0), 3) AS intake_to_enrolled_rate,
  ROUND(SUM(is_enrolled)::numeric / NULLIF(SUM(is_lead), 0), 3) AS lead_to_enrolled_rate
FROM base
GROUP BY 1
ORDER BY lead_to_enrolled_rate DESC, patients DESC;

