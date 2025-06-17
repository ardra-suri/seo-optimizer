# 🔍 SEO Optimizer – Competitor Content Analyzer

[![Render App](https://img.shields.io/badge/Live-Dashboard-brightgreen)](https://seo-optimizer-50y1.onrender.com)

SEO Optimizer is a semantic content comparison tool that helps writers, marketers, and product teams benchmark their content against competitors. It scrapes both pages, performs NLP-powered analysis, and shows which keywords you're missing — helping you close content gaps and improve rankings.


Built with:
- 🔗 Web scraping (`requests`, `BeautifulSoup`)
- 🧠 Semantic analysis (`TensorFlow Hub`, Universal Sentence Encoder)
- 📝 Keyword extraction (`spaCy`, `scikit-learn`)
- 📊 Live dashboard (`Streamlit`, `Plotly`)
- 🗃️ Persistent storage (`SQLite`)
- ✅ CI/CD pipeline (`GitHub Actions`)

---

## 📸 Demo

🔗 **Live App**: [seo-optimizer-yourusername.streamlit.app](https://seo-optimizer-50y1.onrender.com)


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
```

---

## 🚧 Next Steps & Future Enhancements

Below are planned upgrades to make SEO Optimizer more robust, enterprise-ready, and user-friendly:

### 1. User Authentication & Profiles
- Add signup/login (email/password or OAuth via GitHub/Google)  
- Personalize dashboards by user  
- Secure data so each user only views their own analysis history

### 2. Sidebar-based History Viewer
- Use Streamlit’s sidebar to let users:
  - Browse past analyses with filters (date, keyword, similarity score)  
  - Re-run or delete selected entries  
  - Export history as CSV or report
