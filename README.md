# 🛡️ Evaluated LLM Guardrails & Hallucination Benchmark Engine (GenAI Lab 5)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR_STREAMLIT_APP_LINK_HERE.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Groq Fast Inference](https://img.shields.io/badge/Groq-Cloud_Inference-orange.svg)](https://console.groq.com/)

An AI safety, input sanitization, and automated evaluation framework that intercepts prompts, filters malicious prompt injections, redacts sensitive Personally Identifiable Information (PII), and applies an automated LLM-as-a-Judge matrix to score factuality, policy safety, and groundedness.

---

## 🚀 Live Demo

Try the interactive evaluation dashboard:  
👉 **[Launch Streamlit App](https://YOUR_STREAMLIT_APP_LINK_HERE.streamlit.app)**

---

## 📌 Problem Solved

Deploying unconstrained Large Language Models directly in production creates severe risks:
1. **Adversarial Jailbreaks & Injections:** Attackers overriding system constraints to leak backend data or alter logic.
2. **PII & Data Leakage:** Accidental exposure of sensitive user details (emails, phone numbers) sent to external model APIs.
3. **Unchecked Hallucinations:** Factually inaccurate responses presented with high confidence.

This project introduces a **Pre-Execution Interception & Post-Execution LLM-as-a-Judge Architecture** that sanitizes user prompts before inference and evaluates responses across multidimensional safety metrics.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **LLM Engine:** Groq Cloud API (`openai/gpt-oss-20b` / `llama-3.3-70b-versatile`)
* **Evaluation Framework:** LLM-as-a-Judge (Structured JSON schema verification)
* **Data Handling:** Pydantic & Regex Sanitization
* **Web UI:** Streamlit

---

## 📂 Project Structure

```text
GenAI_lab5/
├── .env                  # API keys (kept secret, ignored by git)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Lightweight dependencies
├── eval_engine.py        # Input guardrail logic & LLM-as-a-Judge evaluator
├── app.py                # Streamlit metrics dashboard & evaluation UI
└── README.md             # Project documentation