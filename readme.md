# AI-Powered Comment Moderation System

A multilingual, explainable comment moderation system designed for detecting and handling toxic comments on social media and YouTube, tailored for Times Network.

---

## Features

-  Multilingual support (English, Hindi, Hinglish, more)
-  Advanced AI moderation (XLM-RoBERTa, Perspective API, LLaMA-3)
-  Explainability using LLMs (Groq)
-  Regex & keyword filtering via custom knowledge bases
-  Human review system for borderline cases
-  Streamlined modular pipeline

---

## 📂 Project Structure

```

* KB/                          # Language-specific bad word KBs
* logs/                        # All moderation logs
* .env                         # Store API keys (Groq, Perspective)
* main.py                      # Streamlit or CLI entry point
* api.py                       # FastAPI routes
* pipeline.py                  # Core logic orchestrator
* lang\_detect.py               # Language detection module
* perspective\_ai.py            # Perspective API integration
* bert\_based\_model\_predict.py  # XLM-RoBERTa multilingual model
* llm\_based\_analysis.py        # LLM moderation logic
* explainable\_ai.py            # Groq-based reasoning
* logger.py                    # Logging handler
* model.py                     # HuggingFace model utilities

````

---

## 🛠️ Setup

1. **Clone the repo**

```bash
git clone https://github.com/Dasoam/ModiFiAI.git
cd ModiFiAI/src
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add `.env` file**

```
groq_api=your_groq_key
perspective_api=your_perspective_api_key
db_user=name_for_user
password=DB_password
db_name=Name_for_db

```

---

## How it Works

1. Takes input comment
2. Detects language
3. If English/Hindi → applies regex + KB filtering
4. Otherwise → uses Perspective API + multilingual transformer (XLM-RoBERTa)
5. If toxic → explanation generated via Groq LLaMA-3.3
6. Logs decision → auto block / human review / publish

---

