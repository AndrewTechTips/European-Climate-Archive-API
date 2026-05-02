<div align="center">

  <h1>🌤️ Weather Data API</h1>

  <p>
    A <strong>REST API</strong> built with Flask for querying historical temperature data.<br />
    Real-world climate records from the <strong>European Climate Assessment & Dataset (ECA&D)</strong>,
    served through clean JSON endpoints and documented on a built-in web page.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" />
    <img src="https://img.shields.io/badge/ECA%26D-Real%20Data-blue?style=for-the-badge" alt="ECA&D" />
    <img src="https://img.shields.io/badge/REST%20API-JSON-brightgreen?style=for-the-badge" alt="REST API" />
  </p>

</div>

<br />

---

## 🔌 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Documentation page — lists all available stations |
| `GET` | `/api/v1/<station_id>/<date>` | Temperature for a specific date |
| `GET` | `/api/v1/<station_id>` | All historical data for a station |
| `GET` | `/api/v1/yearly/<station_id>/<year>` | All records for a given year |

**Example request:**
```
GET /api/v1/10/1988-10-25
```
```json
{
  "station": "10",
  "date": "1988-10-25",
  "temperature": 12.4
}
```

---

## ✨ Features

* **📡 3 Query Modes:** Lookup by specific date, full station history, or an entire year.
* **🌡️ Auto-Converted Temperatures:** Raw values are stored as tenths of a degree — the API divides by 10 automatically before returning.
* **🗺️ Station Index Page:** The homepage renders a live table of all available weather stations from `stations.txt`.
* **⚠️ Error Handling:** Returns clean `404` JSON responses for unknown stations or missing dates.

---

## 🧠 Under the Hood

### Reading Station Files
Each station's data lives in a separate `.txt` file with 20 header rows. `utils.py` handles the loading and column cleanup so `main.py` stays clean:

```python
def get_station_data(station_id):
    filename = f"data-small/TG_STAID{str(station_id).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df.columns = [col.strip() for col in df.columns]
    return df
```

### Temperature Conversion
ECA&D stores temperatures as integers in tenths of a degree Celsius — divided by 10 on the way out:

```python
temperature = station_data["TG"].squeeze() / 10
# Raw value: 124 → returned as 12.4°C
```

### Yearly Filter
Date filtering uses pandas `dt.year` accessor, with dates serialized to strings before JSON conversion:

```python
yearly_data = df[df["DATE"].dt.year == int(year)].copy()
yearly_data["DATE"] = yearly_data["DATE"].astype(str)
return yearly_data.to_dict(orient="records")
```

---

## 📁 Project Structure

```
Weather-API/
├── data-small/
│   ├── stations.txt              # List of all weather stations
│   └── TG_STAID000010.txt        # Per-station temperature records
├── templates/
│   └── home.html                 # API documentation & station index
├── main.py                       # Flask app & route definitions
├── utils.py                      # Station file loader
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AndrewTechTips/Weather-API.git
    cd Weather-API
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```bash
    python main.py
    ```

4. **Open in browser:**
    ```
    http://127.0.0.1:5000
    ```

---

## 📬 Contact

* **LinkedIn:** [Andrei Condrea](https://www.linkedin.com/in/andrei-condrea-b32148346)
* **Email:** condrea.andrey777@gmail.com

<p align="center">
  <i>"Real data, real endpoints, real weather." 🌍</i>
</p>