CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS dim_patient (
  patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMP NOT NULL,
  state TEXT,
  age_years INT,
  risk_tier TEXT,
  payer_type TEXT
);
