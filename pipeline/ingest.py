import pandas as pd
import duckdb
from pathlib import Path

# Path relative to the script itself, not where you run it from
csv_path = Path(__file__).parent.parent / "data" / "ventes.csv"
db_path = Path(__file__).parent.parent / "ventes.duckdb"

df = pd.read_csv(csv_path)
con = duckdb.connect(str(db_path))
con.execute("CREATE OR REPLACE TABLE ventes_raw AS SELECT * FROM df")
con.close()
print("Ingestion terminée : ventes_raw créée dans DuckDB")