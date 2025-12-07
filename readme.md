🔍 Smart Fan Share-of-Voice (SoV) Intelligence System

A high-accuracy, Google-powered, multi-keyword share-of-voice engine built using Python, NLP, semantic embeddings, and Streamlit.

This system tracks Atomberg vs competing brands across multiple high-intent search keywords and computes:

Brand mention share (Volume SoV)

Ranking-weighted visibility (Visibility SoV)

Sentiment-weighted positive voice (Positive SoV)

Multi-keyword performance comparison

Brand-specific keyword strengths & weaknesses

Automated insights & marketing recommendations

It uses semantic brand detection (MiniLM embeddings) for ultra-accurate brand recognition across Google search results.

🚀 Features
🔹 High-Accuracy Google-Only Ingestion

Uses SerpAPI to fetch:

Title

Snippet

URL

Google rank

Multi-keyword support

🔹 Advanced Brand Detection

Three-layer detection engine:

Exact alias matching

Fuzzy matching (RapidFuzz)

Semantic brand similarity modeling (Sentence-Transformers MiniLM)

🔹 Snippet-Optimized Sentiment Analysis

DistilBERT sentiment model

Negative trigger words (e.g., “noisy”, “issues”, “expensive”)

Positive trigger words (e.g., “efficient”, “energy saving”)

Hybrid scoring for highest accuracy

🔹 Share of Voice Metrics

For each brand:

Volume SoV

Visibility SoV (log-based rank weight)

Positive Voice SoV

For each keyword:

Brand-wise SoV breakdown

Keyword dominance analysis

🔹 Automated Insights Engine

Generates:

Brand leaders

Sentiment summaries

Keyword strengths/weaknesses

Strategic recommendations

Stored as:

data/insights.md

🔹 Interactive Dashboard (Streamlit)

Visualizes:

SoV charts

Filters (platform, keyword)

Brand distribution

Insights

Raw results table

🧩 Project Structure
smart_fan_sov/
│
├── config.py
├── main.py
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw_google_results.csv
│   ├── sov_summary_global.csv
│   ├── sov_summary_by_keyword.csv
│   └── insights.md
│
├── ingestion/
│   └── google_search.py
│
├── processing/
│   ├── text_cleaning.py
│   ├── brand_detection.py
│   └── sentiment.py
│
├── analytics/
│   ├── sov_metrics.py
│   └── insights.py
│
└── dashboard/
    └── app.py

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/smart_fan_sov.git
cd smart_fan_sov

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Create .env file
SERPAPI_KEY=your_serpapi_key_here
TOP_N=20
KEYWORDS=smart fan,bldc fan,energy saving fan


(Do not commit this file.)

▶️ Run the Pipeline

This fetches Google results, computes SoV, sentiment, insights, and exports CSVs.

python main.py


Outputs:

data/raw_google_results.csv
data/sov_summary_global.csv
data/sov_summary_by_keyword.csv
data/insights.md

📊 Run the Dashboard
streamlit run dashboard/app.py


Features:

Filters by keyword and platform

Global SoV charts

Keyword-level SoV analysis

Raw results explorer

Insights viewer

🧠 Technologies Used

Python

SerpAPI (Google Search API)

Sentence-Transformers (MiniLM embeddings)

Transformers (DistilBERT) – sentiment analysis

RapidFuzz – fuzzy brand matching

NumPy / Pandas – data processing

Streamlit – dashboard

🚧 Roadmap

Planned future upgrades:

Add competitor product-line clustering

Train domain-specific sentiment model

Add scheduled weekly SOV monitoring

Add PDF/Email insights export

Multi-platform extensions (YouTube, Reddit, Instagram via Apify)