

### **Backend**

* **Python** – Core programming language.
* **FastAPI** – For building lightweight REST APIs.
* **Streamlit** – For dashboarding and quick UI previews.

---

### **AI / NLP**

* **Perspective API** – Toxicity scoring and comment analysis.
* **Groq (LLaMA-3)** – Used for explainability (LLM-based reasoning).
* **XLM-RoBERTa / Unity AI Guard** – Multilingual toxicity detection.
* **Regex + Keyword Filters** – For fast, rule-based profanity detection.
* **LangDetect / fastText** – Language detection for comment routing.

---

### **Database / Files**

* **Knowledge Bases** – Hindi, English, Hinglish keyword lists.
* **Log Files** – Stored via `logger.py` in `moderation.log`.
* **Environment Variables** – Secured API keys using `.env`.
* **Mongo DB** – For history.

---

### **Utilities**

* **dotenv** – For environment configuration.
* **Custom Logger** – To track moderation outcomes and errors.
* **ExplainableAI Module** – Converts toxic detections into human-readable reasons.

