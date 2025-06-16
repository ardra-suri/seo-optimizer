# 🔍 SEO Optimizer – Competitor Content Analyzer

[![CI](https://github.com/yourusername/seo-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/seo-optimizer/actions/workflows/ci.yml)
[![Streamlit App](https://img.shields.io/badge/Live-Dashboard-brightgreen)](https://seo-optimizer-yourusername.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

SEO Optimizer is a semantic content comparison tool that helps writers, marketers, and product teams benchmark their content against competitors. It scrapes both pages, performs NLP-powered analysis, and shows which keywords you're missing — helping you close content gaps and improve rankings.


Built with:
- 🔗 Web scraping (`requests`, `BeautifulSoup`)
- 🧠 Semantic analysis (`TensorFlow Hub`, Universal Sentence Encoder)
- 📝 Keyword extraction (`spaCy`, `scikit-learn`)
- 📊 Live dashboard (`Streamlit`, `Plotly`)
- 🗃️ Persistent storage (`SQLite`)
- ✅ CI/CD pipeline (`GitHub Actions`)

---

## 🚀 Features

- ✅ Scrapes content from any public webpage
- 🧠 Compares content against competitor using **USE embeddings**
- 🔍 Extracts top missing SEO keywords
- 🗃️ Saves historical analysis to SQLite
- 📊 Interactive dashboard for exploration
- 🧪 85%+ test coverage with `pytest`
- ☁️ Auto-tested and deployed using **GitHub Actions + Streamlit Cloud**

---

## 🛠️ Tech Stack

| Layer        | Tech                                      |
|--------------|-------------------------------------------|
| Language     | Python 3.10                               |
| Frontend     | Streamlit + Plotly                        |
| Backend      | TensorFlow Hub, spaCy, scikit-learn       |
| Storage      | SQLite (via `sqlite3`)                    |
| DevOps       | GitHub Actions                            |

---

## ⚙️ Getting Started (Local)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/seo-optimizer.git
cd seo-optimizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run dashboard/app.py
