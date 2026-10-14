# 🎓 Campus & Placement AI FAQ Chatbot

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%2B%20Cosine%20Sim-informational.svg)](#how-it-works)

A complete, beginner-friendly **AI FAQ Chatbot for College and Placement Queries** built with **Python**, **Scikit-learn (TF-IDF & Cosine Similarity)**, and a modern, responsive **Streamlit** web interface. 

The chatbot instantly resolves natural language student questions regarding admissions, course curricula, fees, scholarships, semester exams, backlog policies, industrial internships, campus placement eligibility, salary statistics (CTC), and interview preparation.

---

## 📌 Project Highlights

- **🧠 Pure NLP Pipeline (No Paid APIs):** Runs completely offline and locally without OpenAI, Gemini, or any paid API keys.
- **⚡ TF-IDF Vectorization & Cosine Similarity:** Employs unigram/bigram tokenization, sublinear term-frequency scaling, and pattern-level indexing for high matching accuracy.
- **🎛️ Configurable Similarity Threshold:** Interactive slider in the sidebar allows users to dynamically fine-tune the match strictness.
- **🛡️ Smart Fallback & Recommendations:** When a query falls below the threshold, the bot provides a helpful fallback message, campus contact details, and top-3 closest matching FAQ suggestions.
- **💬 Modern Conversational UI:** Clean chat interface featuring chat history, custom avatars, confidence score badges, and a "Clear Chat" action.
- **📚 Rich Preloaded Knowledge Base:** Includes **35+ curated FAQs** categorized across 7 academic and placement domains with multiple phrasing variations (patterns) and tags.
- **📂 Decoupled JSON Architecture:** Knowledge base is stored in a clean JSON file (`faq_data.json`) that can be edited or expanded without modifying application code.
- **🚀 Ready for Portfolio & Resume:** Clean modular code, unit tests, and thorough documentation suitable for software engineering and data science portfolios.

---

## 🏗️ Architecture & NLP Workflow

The application follows an end-to-end information retrieval pipeline:

```
[ User Natural Language Input ]
               │
               ▼
   [ Text Preprocessing ]
   • Lowercasing & whitespace trimming
   • Domain normalization (B.Tech -> btech, C++ -> cpp, T&P -> tnp)
   • Punctuation stripping & English stop-word removal
               │
               ▼
  [ TF-IDF Vectorization ]
   • Unigrams + Bigrams (ngram_range=(1,2))
   • Sublinear term frequency (sublinear_tf=True)
   • Pattern-level index mapping
               │
               ▼
  [ Cosine Similarity Scoring ]
   • Computes dot product against all indexed questions & patterns
   • Max score aggregated per canonical FAQ ID
               │
         ┌─────┴────────────────┐
         ▼                      ▼
[ Score >= Threshold ]   [ Score < Threshold ]
         │                      │
         ▼                      ▼
  [ Matched Answer ]       [ Fallback Message ]
  • Displays Answer        • Rephrasing advice
  • Shows Confidence %     • Top 3 closest suggestions
  • Shows Category Chip    • Official helpdesk contacts
```

---

## 🗂️ Project Directory Structure

```text
college-faq-chatbot/
│
├── app.py               # Streamlit frontend & interactive chat interface
├── nlp_engine.py        # NLP matching engine (TF-IDF, preprocessing, fallback)
├── faq_data.json        # 35+ Curated FAQs with patterns, answers, and tags
├── test_nlp.py          # Standalone automated test suite (100% offline)
├── requirements.txt     # Python dependencies
└── README.md            # Comprehensive documentation & setup guide
```

---

## 🚀 Quickstart Guide (Local Setup)

### 1. Prerequisites
- **Python 3.9 or higher** installed on your system.
- Verify Python installation:
  ```bash
  python --version
  ```

---

### 2. Setup on Windows (PowerShell / Command Prompt)

Open **PowerShell** or **Command Prompt** and navigate to your project directory:

```powershell
# Navigate into the project folder
cd "C:\Users\Abhishek Pawar\.gemini\antigravity\scratch\college-faq-chatbot"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# In PowerShell:
.\venv\Scripts\Activate.ps1
# OR in Command Prompt (cmd.exe):
.\venv\Scripts\activate.bat

# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

> **Note for PowerShell execution policy:** If you encounter `running scripts is disabled on this system`, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```
> and re-run `.\venv\Scripts\Activate.ps1`.

---

### 3. Setup on macOS / Linux

```bash
cd college-faq-chatbot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Running the Chatbot Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at:
👉 **`http://localhost:8501`**

---

### 5. Running the Automated Test Suite

To verify FAQ indexing, NLP matching accuracy, edge cases, and fallback behavior without starting the web UI:

```bash
python test_nlp.py
```

Expected output:
```text
=================================================================
🚀 RUNNING FAQ NLP ENGINE TEST SUITE
=================================================================
[Test 1] Testing FAQ dataset loading & minimum count...
✅ Successfully loaded 35 FAQs.
✅ Categories found (7): Admissions & Eligibility, Campus Facilities & Student Life, Contact & Support, Courses & Academics, Examinations & Evaluation, Fees & Scholarships, Internships & Industry Training, Placement Eligibility & Rules, Placements & Campus Drives
...
🎉 ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)
=================================================================
```

---

## 💬 Sample Questions to Try

You can test the chatbot with varied phrasing and keywords:

| Domain | Natural Language Queries to Test |
| :--- | :--- |
| **Placements** | *"What is the minimum CGPA required for campus placement?"*<br>*"What is the one student one job rule?"*<br>*"Which companies visit for campus placement?"*<br>*"What was the highest package offered?"* |
| **Internships** | *"Are summer internships mandatory?"*<br>*"How do I apply for an NOC for off-campus internship?"* |
| **Fees & Aid** | *"What are the annual tuition fees for B.Tech?"*<br>*"Can I pay semester fees in installments?"*<br>*"What merit scholarships are available?"* |
| **Academics** | *"What is the mandatory attendance requirement?"*<br>*"How is CGPA calculated from SGPA?"*<br>*"What are the rules for clearing ATKT and backlogs?"* |
| **Interview Prep** | *"How should I prepare for technical rounds and DSA?"*<br>*"How to make an ATS-friendly resume for placements?"*<br>*"What are the common rounds in campus recruitment?"* |
| **Fallback Test** | *"How do I bake a chocolate cake?"* *(Triggers fallback & contact guidance)* |

---

## ⚙️ How to Customize or Add New FAQs

Adding new questions does **not** require modifying Python code. Open `faq_data.json` and append an entry to the `"faqs"` list:

```json
{
  "id": 36,
  "category": "Placements & Campus Drives",
  "question": "Does the college provide placement opportunities for postgraduate M.Tech students?",
  "patterns": [
    "Are MTech students eligible for campus placements?",
    "Do companies hire postgraduate M.Tech graduates?",
    "Placement opportunities for M.Tech"
  ],
  "answer": "Yes. Postgraduate M.Tech students participate in placement drives alongside final-year B.Tech students for R&D, core engineering, and specialized data engineering roles.",
  "tags": ["mtech", "postgraduate", "placements", "masters"]
}
```

The next time you refresh the Streamlit page or restart the app, the new question is automatically indexed into the TF-IDF space.

---

## 🎯 Portfolio & Resume Talking Points

If you are showcasing this project on your resume or in technical interviews, consider highlighting these aspects:

1. **Information Retrieval Formulation:** Formulated FAQ answering as an asymmetric text retrieval problem comparing short student queries against curated pattern embeddings.
2. **Sublinear TF Scaling & N-Gram Tokenization:** Implemented unigrams and bigrams (`(1, 2)`) with sublinear term-frequency scaling to prevent common frequent words from dominating domain-specific keywords (e.g. `backlog`, `CGPA`, `NOC`).
3. **Thresholding & Fallback Engineering:** Prevented hallucinations and false positives by enforcing a cosine similarity cutoff with dynamic fallback suggestions and institutional escalations.
4. **Decoupled Architecture:** Followed the Single Responsibility Principle (SRP) by isolating NLP vectorization (`nlp_engine.py`), data persistence (`faq_data.json`), and interactive UI (`app.py`).

---

## 🔮 Limitations & Future Enhancements

- **Contextual Semantic Matching:** Future versions can incorporate lightweight transformer embeddings (e.g., `all-MiniLM-L6-v2` via `sentence-transformers`) for deep semantic understanding.
- **RAG & Generative Integration:** Connect with an open-source LLM (such as Llama 3 or Mistral via Ollama) to synthesize conversational answers grounded in institutional documents.
- **Multi-turn Dialogue Context:** Incorporate dialogue state tracking to handle follow-up questions (e.g., *"What about its fee?"* referring to the previous course).
- **Voice Support:** Add speech-to-text (Web Speech API or Whisper) for spoken voice queries.

---

## ⚠️ Demo Data Disclaimer

All university names, tuition figures, placement statistics, CTC figures, and dates in this repository are **mock demonstration data** created strictly for portfolio and educational demonstration purposes. They do not represent official policies of any specific academic institution.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it for academic and career portfolio purposes.
