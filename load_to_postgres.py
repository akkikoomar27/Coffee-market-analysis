from sqlalchemy import create_engine
import pandas as pd

# Load your cleaned CSV
df = pd.read_csv('final_cleaned.csv')

# ✅ Use your Neon connection string
engine = create_engine(
    "postgresql://neondb_owner:npg_SvpBngb9G8Tt@ep-shiny-thunder-atq1t5e6.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

# Upload to PostgreSQL
df.to_sql('coffee_data', engine, if_exists='replace', index=False)

print("✅ Data uploaded successfully!")

with engine.connect() as conn:
    result = conn.execute("SELECT COUNT(*) FROM coffee_data")

    for row in result:
        print("Total rows:", row[0])
