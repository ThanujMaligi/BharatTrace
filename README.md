# ⚡ BharatTrace
> **AI Terminal Exception Explainer & One-Click Auto-Fix CLI**  
> *Built for the BharatCode Build League 2026 | Powered by BharatCode API (Qwen-27B)*

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![BharatCode](https://img.shields.io/badge/Powered%20By-BharatCode%20API-orange)

Every day, developers waste hours deciphering cryptic compiler outputs, missing dependencies, and multithreaded runtime exceptions. **BharatTrace** bridges the terminal directly to BharatCode's high-speed coding models to explain stack traces and prescribe instant fixes in real time.

---

## 🚀 Key Features
- **Instant Terminal Debugging:** Intercept terminal failures and tracebacks in real-time.
- **Root Cause & Code Diff:** Provides clean root-cause explanations and drop-in code patches.
- **Pipe-Friendly (`stdin`):** Works seamlessly with Unix pipes (`2>&1 | btrace explain`).
- **Context-Aware:** Optionally inspects local source files around the failing line for deep context.
- **Zero Configuration:** Works out of the box with built-in evaluation fallbacks.

---

## 🛠️ Quickstart

### 1. Installation
```bash
git clone https://github.com/ThanujMaligi/BharatTrace.git
cd BharatTrace
pip install -r requirements.txt
```

### 2. Configure BharatCode API Key
```bash
export BHARATCODE_API_KEY="your_api_key_here"
```

### 3. Usage Examples

#### Run any command with automated error catching:
```bash
python btrace.py run "python failing_script.py"
```

#### Pipe any error log directly into BharatTrace:
```bash
python failing_script.py 2>&1 | python btrace.py explain
```

#### Analyze error with local file context:
```bash
python btrace.py explain "KeyError: 'user_id'" --file main.py
```

---

## 🏗️ Architecture
```
[Terminal Error / Stack Trace]
             │
             ▼
      [BharatTrace CLI] ─── (Parses Traceback & Local Source)
             │
             ▼
   [BharatCode Inference API] (Qwen-2.5-Coder / 27B)
             │
             ▼
[Rich Markdown: Root Cause + Code Patch]
```

---

## 👨‍💻 Author
- **Thanuj Kumar Maligi** — [GitHub](https://github.com/ThanujMaligi) | [LinkedIn](https://www.linkedin.com/in/thanuj-kumar-maligi)
- *Amrita Vishwa Vidyapeetham, Bengaluru*
