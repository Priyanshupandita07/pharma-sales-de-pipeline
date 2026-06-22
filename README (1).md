# 💊 Pharma Sales Analytics Pipeline

An end-to-end **Data Engineering pipeline** built on Google Cloud Platform — processing real pharmaceutical sales data from raw CSV to analytics-ready BigQuery tables.

---

## 🏗️ Architecture

```
salesdaily.csv
      ↓
Google Cloud Storage (raw zone)
      ↓  extract()
Pandas ETL (transform)
      ↓  load()
BigQuery (de_practice.pharma_sales)
      ↓
SQL Analytics
```

---

## 📊 Dataset

- **Source:** [Pharma Sales Data — Kaggle](https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data)
- **Size:** 2,106 rows × 13 columns
- **Content:** Daily sales of 8 pharmaceutical drug categories (2014–2019)

| Column | Description |
|--------|-------------|
| `datum` | Date of sales |
| `M01AB`, `M01AE`, `N02BA`, `N02BE`, `N05B`, `N05C`, `R03`, `R06` | Daily sales per drug category |
| `Year`, `Month`, `Hour` | Time components |
| `Weekday Name` | Day of week |

---

## 🔧 Transformations Applied

| Transform | Description |
|-----------|-------------|
| `datum → datetime` | Converted string date to proper datetime type |
| `total_sales` | Sum of all 8 drug sales per day |
| `best_drug` | Highest-selling drug category per day |
| `is_weekend` | Boolean flag for Saturday/Sunday |
| `weekday_name` | Renamed from 'Weekday Name' for BigQuery compatibility |

---

## 📈 Key Insights (from BigQuery SQL Analytics)

| Day | Avg Daily Sales |
|-----|----------------|
| 🥇 Saturday | 65.67 units |
| Sunday | 61.13 units |
| Monday | 60.61 units |
| Friday | 60.25 units |
| Tuesday | 60.02 units |
| Wednesday | 59.24 units |
| 🔻 Thursday | 57.18 units |

- **Saturday** records the highest average daily sales — 15% above Thursday
- **N02BE** (Analgesic/Paracetamol) is the best-selling drug **every single day**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Pipeline orchestration |
| Pandas | Data transformation (ETL) |
| Google Cloud Storage | Raw data storage (landing zone) |
| BigQuery | Cloud data warehouse (analytics layer) |
| google-cloud-bigquery | Python ↔ BigQuery connector |
| google-cloud-storage | Python ↔ Cloud Storage connector |

---

## 🚀 How to Run

### Prerequisites
- Google Cloud account with BigQuery and Cloud Storage enabled
- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Setup
1. Upload `salesdaily.csv` to your Cloud Storage bucket:
```python
from google.cloud import storage
client = storage.Client(project="your-project-id")
bucket = client.bucket("your-bucket-name")
blob = bucket.blob("raw/salesdaily.csv")
blob.upload_from_filename("salesdaily.csv")
```

2. Update `CONFIG` in `pipeline.py`:
```python
PROJECT_ID  = "your-project-id"
BUCKET_NAME = "your-bucket-name"
BQ_TABLE    = "your_dataset.pharma_sales"
```

3. Run the pipeline:
```bash
python pipeline.py
```

---

## 📁 Project Structure

```
pharma-sales-de-pipeline/
├── pipeline.py        ← ETL pipeline (extract → transform → load)
├── requirements.txt   ← Python dependencies
└── README.md          ← Project documentation
```

---

## 👤 Author

**Priyanshu Pandita**
- GitHub: [@Priyanshupandita07](https://github.com/Priyanshupandita07)
- LinkedIn: [priyanshu-pandita](https://linkedin.com/in/priyanshu-pandita)
