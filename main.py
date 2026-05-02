from flask import Flask, render_template, jsonify
import pandas as pd

from utils import get_station_data

app = Flask(__name__)

stations = pd.read_csv("data-small/stations.txt", skiprows=17)
stations.columns = [col.strip() for col in stations.columns]
stations = stations[["STAID", "STANAME"]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = get_station_data(station)
    if df is None:
        return jsonify({"error": "Station not found"}), 404

    station_data = df.loc[df["DATE"] == date]

    if station_data.empty:
        return jsonify({"error": "Date not found for this station"}), 404

    temperature = station_data["TG"].squeeze() / 10
    return {"station": station, "date": date, "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    df = get_station_data(station)
    if df is None:
        return jsonify({"error": "Station not found"}), 404

    return df.to_dict(orient="records")


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data-small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    return result.to_dict(orient="records")


if __name__ == "__main__":
    app.run(debug=True)
