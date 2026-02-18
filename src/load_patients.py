import random
from datetime import datetime, timedelta
from uuid import uuid4

import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://chelseaharmon@localhost:5432/maternal_growth"

STATES = ["CA", "WA", "OR", "NY", "TX", "FL", "IL", "MA", "CO", "GA"]
RISK_TIERS = ["low", "medium", "high"]
PAYER_TYPES = ["commercial", "medicaid", "self_pay"]

def generate_patients(n=1000):
    now = datetime.now()
    rows = []

    for _ in range(n):
        created_at = now - timedelta(days=random.randint(0, 365))
        age_years = random.randint(18, 45)
        risk_tier = random.choices(RISK_TIERS, weights=[0.6, 0.3, 0.1])[0]
        payer_type = random.choices(PAYER_TYPES, weights=[0.7, 0.25, 0.05])[0]
        state = random.choice(STATES)

        rows.append({
            "patient_id": str(uuid4()),
            "created_at": created_at,
            "state": state,
            "age_years": age_years,
            "risk_tier": risk_tier,
            "payer_type": payer_type
        })

    return pd.DataFrame(rows)

def main():
    df = generate_patients(1000)
    engine = create_engine(DB_URL)
    df.to_sql("dim_patient", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} patients.")

if __name__ == "__main__":
    main()

