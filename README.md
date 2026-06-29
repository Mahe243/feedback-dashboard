# 💬 Customer Feedback Dashboard

A Streamlit app with real-time sentiment analysis using **TextBlob** and interactive charts via **Plotly**.

---

## 📁 Project Structure

```
feedback_dashboard/
│
├── app.py               ← Main Streamlit application
├── seed_data.py         ← Script to pre-populate sample data
├── requirements.txt     ← Python dependencies
├── README.md            ← This file
└── data/
    └── feedbacks.json   ← Auto-created on first run
```

---

## ⚙️ Setup & Run in VS Code

### Step 1 — Open project in VS Code
```bash
cd feedback_dashboard
code .
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Download TextBlob corpora (one-time)
```bash
python -m textblob.download_corpora
```

### Step 5 — (Optional) Pre-populate sample data
```bash
python seed_data.py
```

### Step 6 — Launch the app
```bash
streamlit run app.py
```

The app opens automatically at → **http://localhost:8501**

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📊 Dashboard | KPI metrics, sentiment pie, rating bar, scatter, trend line, category heatmap |
| ➕ Add Feedback | Form with live sentiment gauge using TextBlob |
| 📋 All Feedbacks | Filter by sentiment/category, search by keyword, export CSV |

---

## 🛠 Tech Stack
- **Streamlit** — Web UI framework
- **TextBlob** — NLP sentiment analysis
- **Plotly** — Interactive charts
- **Pandas** — Data manipulation
- **JSON** — Lightweight local storage
