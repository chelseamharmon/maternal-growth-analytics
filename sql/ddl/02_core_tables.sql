-- 1) Where patients came from (marketing / referral)
CREATE TABLE IF NOT EXISTS dim_acquisition_channel (
  channel_id SERIAL PRIMARY KEY,
  channel_name TEXT UNIQUE NOT NULL,     -- e.g., paid_search, ob_referral, employer, organic
  channel_type TEXT NOT NULL             -- paid, referral, partnership, organic
);

-- 2) Enrollment + lifecycle status (one row per patient)
CREATE TABLE IF NOT EXISTS fact_patient_lifecycle (
  patient_id UUID PRIMARY KEY REFERENCES dim_patient(patient_id),
  channel_id INT REFERENCES dim_acquisition_channel(channel_id),
  lead_created_at TIMESTAMP,
  eligibility_verified_at TIMESTAMP,
  intake_completed_at TIMESTAMP,
  enrolled_at TIMESTAMP,
  churned_at TIMESTAMP,
  churn_reason TEXT,
  is_active BOOLEAN NOT NULL DEFAULT FALSE
);

-- 3) Event stream (product/care engagement)
CREATE TABLE IF NOT EXISTS fact_patient_event (
  event_id BIGSERIAL PRIMARY KEY,
  patient_id UUID NOT NULL REFERENCES dim_patient(patient_id),
  event_ts TIMESTAMP NOT NULL,
  event_name TEXT NOT NULL,              -- e.g., message_sent, visit_completed, care_plan_created
  event_source TEXT,                     -- app, sms, clinician, support
  event_metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_event_patient_ts ON fact_patient_event(patient_id, 
event_ts);
CREATE INDEX IF NOT EXISTS idx_event_name_ts ON fact_patient_event(event_name, event_ts);

