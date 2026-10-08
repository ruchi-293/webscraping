from flask import Flask, jsonify, render_template
from pathlib import Path
import pandas as pd

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "ipl_data.csv"

EXPECTED_COLUMNS = [
    "Player Name", "Matches", "Runs", "Batting Avg", "Wickets", "Bowling Avg"
]

def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    df = pd.read_csv(DATA_FILE)
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = 0 if col != "Player Name" else ""
    for col in EXPECTED_COLUMNS[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["Player Name"] = df["Player Name"].astype(str)
    return df[EXPECTED_COLUMNS]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    df = load_data()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/summary")
def api_summary():
    df = load_data()
    if df.empty:
        return jsonify({
            "players": 0, "total_matches": 0, "total_runs": 0,
            "top_run_scorer": "-", "top_bowler": "-"
        })

    top_runs = df.sort_values("Runs", ascending=False).iloc[0]
    top_wickets = df.sort_values("Wickets", ascending=False).iloc[0]

    return jsonify({
        "players": int(len(df)),
        "total_matches": int(df["Matches"].max()) if len(df) else 0,
        "total_runs": int(df["Runs"].sum()),
        "top_run_scorer": top_runs["Player Name"],
        "top_bowler": top_wickets["Player Name"]
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
