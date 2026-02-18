import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://chelseaharmon@localhost:5432/maternal_growth"

FUNNEL_STAGES = ["lead_created_at", "eligibility_verified_at", "intake_completed_at", "enrolled_at"]

CHANNEL_DROP = {
    "paid_search": 0.65,
    "paid_social": 0.55,
    "ob_referral": 0.78,
    "employer": 0.72,
    "organic": 0.60,
    "partner_clinic": 0.75,
}

def main():
    engine = create_engine(DB_URL)

    # Pull patients
    patients = pd.read_sql("SELECT patient_id, created_at, risk_tier FROM dim_patient", engine)
    if patients.empty:
        raise RuntimeError("dim_patient is empty. Run load_patients.py first.")

    # Pull channels
    channels = pd.read_sql("SELECT channel_id, channel_name FROM dim_acquisition_channel", engine)
    channel_map = dict(zip(channels["channel_name"], channels["channel_id"]))

    rows_lifecycle = []
    rows_events = []

    now = datetime.now()

    for _, r in patients.iterrows():
        patient_id = r["patient_id"]
        created_at = pd.to_datetime(r["created_at"]).to_pydatetime()
        risk = r["risk_tier"]

        # Assign channel
        channel_name = random.choices(
            list(CHANNEL_DROP.keys()),
            weights=[0.22, 0.18, 0.18, 0.12, 0.20, 0.10],
        )[0]
        channel_id = channel_map[channel_name]

        # Simulate funnel timestamps with drop-off
        lead_created_at = created_at + timedelta(hours=random.randint(0, 48))
        prob_enroll = CHANNEL_DROP[channel_name]

        # Risk impacts enrollment slightly
        if risk == "high":
            prob_enroll -= 0.06
        elif risk == "low":
            prob_enroll += 0.03

        def maybe_time(prev, min_h, max_h, p):
            if random.random() <= p:
                return prev + timedelta(hours=random.randint(min_h, max_h))
            return None

        eligibility_verified_at = maybe_time(lead_created_at, 6, 120, 0.85)
        intake_completed_at = (
            maybe_time(eligibility_verified_at, 6, 168, 0.80) if eligibility_verified_at else None
        )
        enrolled_at = (
            maybe_time(intake_completed_at, 1, 72, prob_enroll) if intake_completed_at else None
        )

        # Churn model (only if enrolled)
        churned_at = None
        churn_reason = None
        is_active = False

        if enrolled_at:
            # churn probability varies with channel + risk
            churn_p = 0.18
            if channel_name in ("paid_social",):
                churn_p += 0.04
            if risk == "high":
                churn_p += 0.05

            if random.random() < churn_p:
                churned_at = enrolled_at + timedelta(days=random.randint(7, 90))
                churn_reason = random.choice(["no_longer_needed", "cost", "switched_provider", "low_engagement"])
                is_active = False
            else:
                is_active = True

            # engagement events (weekly-ish) until churn or now
            end_ts = churned_at or now
            t = enrolled_at
            while t < end_ts:
                t += timedelta(days=random.randint(3, 10))
                if t >= end_ts:
                    break
                event_name = random.choices(
                    ["message_sent", "visit_completed", "care_plan_created", "check_in_completed"],
                    weights=[0.45, 0.25, 0.15, 0.15],
                )[0]
                rows_events.append(
                    {
                        "patient_id": patient_id,
                        "event_ts": t,
                        "event_name": event_name,
                        "event_source": random.choice(["app", "sms", "clinician", "support"]),
                        "event_metadata": None,
                    }
                )

        rows_lifecycle.append(
            {
                "patient_id": patient_id,
                "channel_id": channel_id,
                "lead_created_at": lead_created_at,
                "eligibility_verified_at": eligibility_verified_at,
                "intake_completed_at": intake_completed_at,
                "enrolled_at": enrolled_at,
                "churned_at": churned_at,
                "churn_reason": churn_reason,
                "is_active": is_active,
            }
        )

    lifecycle_df = pd.DataFrame(rows_lifecycle)
    events_df = pd.DataFrame(rows_events)

    # Upsert lifecycle (delete + insert for simplicity in a local portfolio project)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_patient_event RESTART IDENTITY;"))
        conn.execute(text("TRUNCATE TABLE fact_patient_lifecycle;"))

    lifecycle_df.to_sql("fact_patient_lifecycle", engine, if_exists="append", index=False)
    if not events_df.empty:
        events_df.to_sql("fact_patient_event", engine, if_exists="append", index=False)

    print(f"Loaded lifecycle rows: {len(lifecycle_df)}")
    print(f"Loaded event rows: {len(events_df)}")

if __name__ == "__main__":
    main()

