# 🤖 AutoReviewBot

**Modular, Extensible, and AI-Ready System for Automated Code Review on GitHub**

---

## 📌 Overview

**AutoReviewBot** is an end-to-end automated pull request (PR) review system designed to improve code quality, enforce coding standards, and scale code review in collaborative environments. It combines **static rule-based analysis** with a roadmap for **LLM-powered semantic code review** and features:

- ✅ GitHub App integration for real-time PR analysis  
- ✅ Inline code comments for violations  
- ✅ Severity-aware check runs and merge blocking  
- ✅ YAML-driven modular rule engine  
- ✅ CI/CD-ready with GitHub Actions  
- ✅ Dockerized microservice architecture  

---

## 📂 Repository Structure
```
.
├── README.md
├── Stirling-PDF
│   ├── AllViolationsTrigger.java
│   └── FinalBlockTest.java
├── app
│   └── main.py
├── config
│   ├── github_app.yaml
│   └── java_rules.yaml
├── docker
│   └── Dockerfile
├── docker-compose.yml
├── metrics
│   └── logger.py
├── requirements.txt
├── rules
│   ├── java_style_rules.yaml
│   └── loader.py
├── tests
│   └── test_autoreviewbot.py
└── tools
    ├── github_api.py
    ├── github_auth.py
    ├── linter.py
    └── review.py
```

---

## 🛠️ System Architecture

### ✅ Components

| Component           | Description |
|---------------------|-------------|
| **Webhook Server**  | Built with FastAPI; receives & verifies PR events |
| **Analysis Pipeline** | Fetches Java files using GitHub Contents API |
| **Rule Engine**     | YAML-based, regex-driven static analyzer |
| **Logger**          | Saves violations to `violations.csv` & `violations.jsonl` |
| **Commenter**       | Posts inline GitHub PR comments for each violation |
| **CI/CD Workflow**  | GitHub Actions for bot testing & deployment |
| **Containerized**   | Docker-ready with plug-and-play setup |

---

## 📏 Rule Engine

AutoReviewBot supports 14 static rules for Java (stored in `rules/java_style_rules.yaml`), each defined by:

- `rule_id`: Unique identifier (e.g., `JAVA-001`)
- `pattern`: Regex or syntax pattern
- `severity`: `high`, `medium`, `low`
- `suggestion`: Human-readable remediation

### ✅ Sample rules

| Rule ID   | Pattern                     | Severity | Suggestion                                       |
|-----------|-----------------------------|----------|--------------------------------------------------|
| JAVA-001  | `System\.out\.print`        | Medium   | Use a logger instead of `System.out.print`       |
| JAVA-002  | `== null`                   | High     | Use `Objects.isNull()` instead                   |
| JAVA-007  | `Vector<`                   | Low      | Prefer `ArrayList` over `Vector`                |
| JAVA-014  | `this.var = var;`           | High     | Avoid mutable state leaks; use defensive copy   |

➡️ [View all rules here](rules/java_style_rules.yaml)

---

## ✅ Key Features & Validations

| Feature                         | Status | PRs |
|----------------------------------|--------|-----|
| GitHub App Integration          | ✅     | [#23](https://github.com/PushkrJain/Stirling-PDF/pull/23), [#22](https://github.com/PushkrJain/Stirling-PDF/pull/22) |
| Java File Parsing               | ✅     | [#23](https://github.com/PushkrJain/Stirling-PDF/pull/23), [#22](https://github.com/PushkrJain/Stirling-PDF/pull/22) |
| Static Rule Engine              | ✅     | [#22](https://github.com/PushkrJain/Stirling-PDF/pull/22) |
| Inline PR Comments              | ✅     | [#23](https://github.com/PushkrJain/Stirling-PDF/pull/23), [#22](https://github.com/PushkrJain/Stirling-PDF/pull/22) |
| Check Runs + Merge Gating       | ✅     | [#12](https://github.com/PushkrJain/Stirling-PDF/pull/12) |
| Violation Logging               | ✅     | [#7](https://github.com/PushkrJain/Stirling-PDF/pull/7) |
| Stress Testing (3000+ LOC)      | ✅     | [#13](https://github.com/PushkrJain/Stirling-PDF/pull/13) |
| Maintainer Override             | ✅     | [#6](https://github.com/PushkrJain/Stirling-PDF/pull/6) |

---

## 🚀 Quick Start (Local Setup)

```bash
# 1. Clone the repository
git clone https://github.com/PushkrJain/autoreviewbot.git
cd autoreviewbot

# 2. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run the webhook server
uvicorn main:app --reload

```
---

## 🔐 GitHub App Setup

To test webhook end-to-end:

1. **Create a GitHub App**
   - Set the **Webhook URL** to your public endpoint (e.g., ngrok)
   - Enable the following **events**:
     - `pull_request`
     - `check_run`
     - `check_suite`

2. **Store the following secrets in the `config/` directory**:
```
config/
├── app_id.txt # Your GitHub App ID
├── private-key.pem # Your GitHub App's private key
└── webhook_secret.txt # Your webhook secret
```

3. **Expose local FastAPI server using ngrok**:
```bash
ngrok http 8000
```
---

## 🔭 Roadmap (Phase 2)

- 🔁 **Feedback loop** for rule override & false positive learning  
- 🧠 **LLM-powered smart comments** (e.g., Mistral, CodeLlama)  
- 📊 **Grafana dashboards** via Prometheus  
- 🌐 **Multi-language support** via plug-in agents  
- ✉️ **Slack/Teams integration**

---

## 🧠 Future Vision

**AutoReviewBot** aims to be a **practical**, **explainable**, and **high-performance** alternative to closed-source tools like **CodeRabbit**, **Sourcery**, and **Amazon CodeGuru**.

- ✅ YAML-defined rules  
- ✅ Transparent inline feedback  
- ✅ GitHub-native merge blocking  
- ✅ Metrics-driven learning

