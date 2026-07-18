# 💬 Customer Feedback Dashboard

A Streamlit app with real-time sentiment analysis using **TextBlob** and interactive charts via **Plotly**.

## 🌐 Live Demo

**Try the live application here:**  
https://feedback-dashboard-8pxjp5jetwn5emryki4xms.streamlit.app/

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

## Proof of Execution
<img width="1403" height="929" alt="Screenshot 2026-07-03 153949" src="https://github.com/user-attachments/assets/ae4b05da-e1ff-486c-ba9a-352ac642eb05" />
<img width="1465" height="749" alt="Screenshot 2026-07-03 153937" src="https://github.com/user-attachments/assets/011b3c4a-43a3-47d8-af70-2167cbf3f442" />
<img width="1432" height="701" alt="Screenshot 2026-07-03 153924" src="https://github.com/user-attachments/assets/01b55012-059f-4252-804d-908d86b6277b" />
<img width="1833" height="530" alt="Screenshot 2026-07-03 153913" src="https://github.com/user-attachments/assets/d96b49fc-ff97-4620-aef5-dd4b4092c784" />
