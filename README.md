<div align="center">

```
██╗   ██╗██████╗ ██╗      ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗███╗   ██╗███████╗██████╗
██║   ██║██╔══██╗██║      ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔════╝██╔══██╗
██║   ██║██████╔╝██║      ███████╗███████║██║   ██║██████╔╝   ██║   █████╗  ██╔██╗ ██║█████╗  ██████╔╝
██║   ██║██╔══██╗██║      ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║███████╗ ███████║██║  ██║╚██████╔╝██║  ██║   ██║   ███████╗██║ ╚████║███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
```

### ⚡ Production-hardened URL shortener. Built fast. Audited harder.

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)

[![Security Audit](https://img.shields.io/badge/Security_Audit-PASSED-00C851?style=for-the-badge&logo=shieldsdotio&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)]()
[![Deploy](https://img.shields.io/badge/Deploy-Railway-blueviolet?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

</div>

---

<div align="center">
  <h3>🔗 Shorten &nbsp;·&nbsp; 📊 Track &nbsp;·&nbsp; 🛡️ Secure &nbsp;·&nbsp; 🐳 Deploy</h3>
</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🛡️ Security Audit](#️-security-audit)
- [📁 Project Structure](#-project-structure)
- [⚙️ API Reference](#️-api-reference)
- [🐳 Run with Docker](#-run-with-docker)
- [🌍 Deployment](#-deployment)
- [🔧 Environment Variables](#-environment-variables)
- [🧱 Tech Stack](#-tech-stack)
- [📌 Roadmap](#-roadmap)

---

## ✨ Features

```
🔗  Shorten any URL → clean 8-char slug
📊  Per-slug click analytics
🛡️  Self-audited security hardening
🐳  One command Docker setup
⚡  Async FastAPI — fast as hell
🗃️  PostgreSQL with Alembic migrations
🔁  Atomic click counter — no race conditions
```

---

## 🛡️ Security Audit

> *"Working and production-ready are not the same thing."*

Before pushing to production, I put on the attacker hat and went through the entire app. Here's the full audit report:

<br/>

| 🔍 | Vulnerability | Severity | Status |
|:--:|--------------|:--------:|:------:|
| 1 | **No rate limiting** — `/shorten` wide open for mass slug generation | 🔴 High | ✅ Fixed |
| 2 | **Slug enumeration** — 6-char keyspace (~56B) is bruteforceable | 🟡 Medium | ✅ Fixed |
| 3 | **SSRF via URL input** — `file://`, `javascript://` accepted | 🔴 Critical | ✅ Fixed |
| 4 | **AWS metadata exposure** — `169.254.169.254` not blocked | 🔴 Critical | ✅ Fixed |
| 5 | **Path traversal on slugs** — special chars not rejected | 🟡 Medium | ✅ Fixed |
| 6 | **Click counter race condition** — read-modify-write under load | 🟢 Low | ✅ Fixed |
| 7 | **DB session leaks** — `db.close()` skipped on exceptions | 🟡 Medium | ✅ Fixed |
| 8 | **Zero security headers** — no CSP, server fingerprint exposed | 🟡 Medium | ✅ Fixed |
| 9 | **No request size limit** — oversized bodies hit the app | 🟢 Low | ✅ Fixed |

<br/>

### 🔒 What the fixes look like

**Rate Limiting** — Sliding-window counter per IP, per endpoint:
```
POST /shorten   →  10 req / min / IP
GET  /{slug}    →  60 req / min / IP
GET  /stats     →  30 req / min / IP
```

**SSRF Protection** — Multi-layer URL validation:
```python
BLOCKED_SCHEMES  →  file, javascript, data, ftp, vbscript, blob
BLOCKED_HOSTS    →  localhost, 169.254.169.254, metadata.google.internal
PRIVATE_RANGES   →  127.x, 10.x, 172.16-31.x, 192.168.x, 169.254.x, ::1
```

**Security Headers** — Applied to every single response:
```
X-Content-Type-Options    →  nosniff
X-Frame-Options           →  DENY
X-XSS-Protection          →  1; mode=block
Content-Security-Policy   →  default-src 'none'; frame-ancestors 'none'
Referrer-Policy           →  strict-origin-when-cross-origin
Server header             →  stripped (no fingerprinting)
```

**Slug Hardening:**
```
Before  →  6 chars  →  ~56,000,000,000 combinations
After   →  8 chars  →  ~218,000,000,000,000 combinations
Regex   →  ^[A-Za-z0-9]{6,16}$ enforced before DB is ever touched
```

---

## 📁 Project Structure

```
url-shortener/
│
├── 🐍 main.py                  # FastAPI app — routes, middleware, security
├── 🗃️  models.py                # SQLAlchemy URL model
├── 🔌 database.py              # Engine + session factory
│
├── 📦 alembic/                 # DB migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── 🐳 Dockerfile               # Python 3.12 image
├── 🐳 docker-compose.yml       # App + PostgreSQL orchestration
├── 📋 requirements.txt
├── ⚙️  alembic.ini
└── 🔑 .env                     # Local secrets (never commit)
```

---

## ⚙️ API Reference

### `POST /shorten`
> Shorten a URL and get a slug back.

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/some/very/long/url"}'
```

```json
{
  "short_code": "aB3xKp9Z",
  "url": "https://example.com/some/very/long/url",
  "clicks": 0
}
```

---

### `GET /{slug}`
> Redirects to original URL. Click count incremented atomically.

```bash
curl -L http://localhost:8000/aB3xKp9Z
# → 301 Redirect to original URL
```

---

### `GET /stats/{slug}`
> Fetch analytics for a slug.

```bash
curl http://localhost:8000/stats/aB3xKp9Z
```

```json
{
  "short_code": "aB3xKp9Z",
  "url": "https://example.com/some/very/long/url",
  "clicks": 42
}
```

---

### `GET /health`
> DB-connected health check.

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

---

## 🐳 Run with Docker

> **Prerequisites:** Docker + Docker Compose

```bash
# Clone
git clone https://github.com/crazycodesucker/url-shortener.git
cd url-shortener

# Build & run
docker compose up --build
```

```
✅ App  →  http://localhost:8000
📚 Docs →  http://localhost:8000/docs
```

```bash
# Stop
docker compose down

# Stop + wipe DB volume
docker compose down -v
```

---

## 🌍 Deployment

### 🚂 Railway — Recommended (Free, ~10 min)

```
1.  Push repo to GitHub
2.  railway.app → New Project → Deploy from GitHub repo
3.  Add PostgreSQL plugin from the Railway dashboard
4.  DATABASE_URL is injected automatically as an env var
5.  Hit Deploy → done ✅
```

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

---

### ☁️ AWS EC2 (Free Tier)

```bash
# 1. Launch t2.micro (Ubuntu 22.04) on EC2

# 2. SSH in
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# 3. Install Docker
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu && newgrp docker

# 4. Clone & run
git clone https://github.com/crazycodesucker/url-shortener.git
cd url-shortener
docker compose up -d --build

# 5. Open port 8000 in your EC2 Security Group (inbound rule)
```

```
✅ Live at → http://YOUR_EC2_IP:8000
```

> 💡 **Production tip:** Put Nginx in front, point a domain at it, terminate SSL at the load balancer.

---

### 🟣 Render (Free Tier Alternative)

```
1.  render.com → New Web Service → Connect GitHub repo
2.  Add PostgreSQL addon
3.  Set DATABASE_URL in environment variables
4.  Deploy ✅
```

---

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

**Local `.env` file:**
```env
DATABASE_URL=postgresql://postgres:admin@db:5432/url_shortener
```

> ⚠️ `.env` is in `.gitignore`. Never push credentials to GitHub.

---

## 🧱 Tech Stack

<div align="center">

| Layer | Technology | Version |
|:-----:|-----------|:-------:|
| 🚀 Framework | FastAPI | Latest |
| 🗃️ Database | PostgreSQL | 17 |
| 🔌 ORM | SQLAlchemy | Latest |
| 🔄 Migrations | Alembic | Latest |
| 🐍 Runtime | Python | 3.12 |
| ⚡ Server | Uvicorn | Latest |
| 🐳 Container | Docker + Compose | Latest |

</div>

---

## 📌 Roadmap

```
✅  Core URL shortening
✅  Click tracking
✅  Docker setup
✅  Security hardening + audit

⬜  Owner tokens for private stats
⬜  Custom slug support
⬜  Redis-backed rate limiting (multi-worker)
⬜  Slug expiry / TTL
⬜  Frontend UI
⬜  QR code generation per slug
```

---

## 👤 Author

<div align="center">

**crazycodesucker**

Backend Developer · Security-First Mindset

[![GitHub](https://img.shields.io/badge/GitHub-crazycodesucker-181717?style=for-the-badge&logo=github)](https://github.com/crazycodesucker)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yourprofile)

</div>

---

<div align="center">

*Built with a security-first mindset. Because shipping broken is worse than shipping late.*

</div>
