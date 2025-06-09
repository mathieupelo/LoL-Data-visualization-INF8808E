from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/api/wins-by-player')
def wins_by_player():
    df = pd.read_csv("data.csv")

    player = request.args.get('player', default=None, type=str)
    if player:
        df = df[df["PlayerName"] == player]

    grouped = df.groupby("Champion")["Win"].sum().sort_values(ascending=False)
    return jsonify(grouped.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
