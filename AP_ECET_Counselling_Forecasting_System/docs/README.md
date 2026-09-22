# AP ECET Counselling Forecasting System 🎓

A full-stack, data-driven lateral entry admission forecasting and decision-support web application for diploma students appearing for the Andhra Pradesh Engineering Common Entrance Test (**AP ECET**).

Built for the Department of Technical Education & Andhra Pradesh State Council of Higher Education (APSCHE) ecosystem.

> **Audit & Enhancement (Sept 2026)**  
> All 28 official features are covered end-to-end.  
> Hybrid forecasting now blends recency-weighted historical cutoffs with trained Random Forest / Decision Tree / Linear Regression models.  
> Admin CRUD expanded (colleges edit, branches edit, seat-matrix add/delete, notifications create, calendar management).  
> Change-password, improved forgot-password recovery, and OpenStreetMap college location links added.  
> `requirements.txt` included. All automated tests pass.

---

## 🌟 Key Features

### 1. 🎯 Hybrid Admission Forecasting Engine
- **Multi-Model Machine Learning Architecture**:
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
- **Explainable AI (XAI) Classifications**:
  - 🟢 **Safe (80%–100%)**: High probability of seat allotment based on rank and cutoff history.
  - 🟡 **Moderate (50%–79%)**: Competitive chances; subject to phase movements.
  - 🟠 **Ambitious (25%–49%)**: Reach options with aggressive cutoff trends.
  - 🔴 **Dream (< 25%)**: Top-tier aspirational institutions.
- Multi-parametric matching on **Rank, Category, Gender, Region (AU / SVU / UR), Round (Phase 1, Phase 2, Final Phase), District, and College Type**.

### 2. 🔐 Separated Role-Based Portals & Guards
- **Candidate Portal (`/login`)**:
  - Dedicated sign-in for AP ECET aspirants.
  - Immediate post-login redirection to candidate profile configuration.
  - Modern Lucide SVG password visibility toggles (no emojis).
  - Quick link to Examination Officer portal.
- **Administrator Back-Office Portal (`/admin/login`)**:
  - Dedicated authentication for Examination Officers and administrators.
  - **Role Guard Protection**: Automatically blocks student credentials and safely redirects them to the Candidate Portal.
  - Management of colleges, branches, cutoff records, seat matrices, and batch CSV uploads.

### 3. 👤 Dynamic Profile Management & Left Drawer Navigation
- **11-Parameter Candidate Profile** (styled per AP ECET design specs):
  1. Username
  2. Mobile Number
  3. AP ECET State Rank
  4. Category (`OC`, `BC-A`, `BC-B`, `BC-C`, `BC-D`, `BC-E`, `SC`, `ST`, `EWS`)
  5. Gender (`Boys`, `Girls`)
  6. Local Area (`AU — Andhra University`, `SVU — Sri Venkateswara University`, `UR — Statewide / Non-Local`)
  7. Diploma Branch (`Computer Engineering`, `ECE`, `EEE`, `Mechanical`, `Civil`, `IT`, etc.)
  8. Preferred B.Tech Branch (`CSE`, `AI&ML`, `Data Science`, `IT`, `ECE`, etc.)
  9. Alternative Branch
  10. Preferred District
  11. College Type Preference (`Govt / University`, `Autonomous`, `Private`, `Any`)
- **Sliding Left Navigation Drawer (☰)**:
  - Clean top header with hamburger toggle button (three straight lines), brand identity, theme switcher, and profile status.
  - Sliding drawer navigation with dark backdrop overlay for quick access to all candidate tools.

### 4. 🔮 What-If Counselling Simulator
- Run side-by-side comparative scenarios testing variations in:
  - Candidate rank adjustments
  - Primary vs. secondary branch choices
  - Counselling phase progression (Phase 1 vs. Final Phase)
  - Quota movements across university regions

### 5. 📋 Smart Preference List Generator & Exporter
- Build, reorder, and curate web options preference lists.
- Instant export to:
  - **Official Formatted PDF** (with college codes, district tags, and probabilities)
  - **CSV Spreadsheet** for offline web counseling verification.

### 6. 📊 Cutoff Analytics & Trend Visualizer
- Multi-year cutoff trends covering:
  - **Historical Data**: 2023, 2024
  - **AI Forecasted Trends**: 2025, 2026
- Interactive Chart.js visualizations by college, branch, and category.

### 7. ⭐ Admin Viva & Model Evaluation Reports
- Comprehensive ML performance breakdown:
  - Mean Absolute Error (**MAE**)
  - Root Mean Squared Error (**RMSE**)
  - Coefficient of Determination (**R² Score**)
  - Classification **F1-Score**

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask |
| **Database** | SQLite3 (`ap_ecet.db`) with custom indexing (portable alternative to MySQL) |
| **Machine Learning** | Scikit-learn (Linear / Decision Tree / Random Forest) — hybrid inference + viva metrics |
| **Frontend** | Semantic HTML5, Vanilla CSS3 (Dark/Light mode), Modern JavaScript (ES6+) |
| **Charts** | Chart.js 4.4+ |
| **PDF Engine** | ReportLab |
| **Maps** | OpenStreetMap search links for college locations |
| **Icons & Design** | Lucide-inspired SVG vectors, Glassmorphism UI tokens |

---

## 📂 Project Structure

```text
AP_ECET_Counselling_Forecasting_System/
├── app.py                     # Master Flask web application & route controllers
├── wsgi.py                    # WSGI entry point for production (Gunicorn)
├── config.py                  # Central configuration (DB, OTP, security)
├── database.py                # SQLite connection manager, table schemas & indexes
├── forecasting_engine.py      # ML pipeline, regression models, and XAI scoring
├── pdf_generator.py           # ReportLab PDF report generation utilities
├── otp_service.py             # OTP generation & delivery (email/SMS/demo)
├── etl_ingest.py              # Data ingestion from Excel into SQLite
├── requirements.txt           # Python dependencies
├── Procfile / render.yaml     # Deployment configs
├── .env.example               # Environment variable template
│
├── data/                      # Data assets (do not commit secrets)
│   ├── ap_ecet.db             # Seeded SQLite database
│   ├── colleges_details.xlsx  # Master college & branch information
│   └── cutoffs/
│       ├── cutoffs_2023.xlsx
│       ├── cutoffs_2024.xlsx
│       ├── cutoffs_2025.xlsx
│       └── cutoffs_2026.xlsx
│
├── static/
│   ├── css/
│   │   └── style.css          # Design system, glassmorphism tokens, responsive layout
│   └── js/
│       └── main.js            # Theme toggle, charts, OTP UI, preference list logic
│
├── templates/
│   ├── base.html              # Base shell, sliding drawer, header & modals
│   ├── index.html / home.html # Landing page
│   ├── auth/                  # Login, register, forgot/change password
│   ├── student/               # Candidate portal pages
│   └── admin/                 # Admin back-office pages
│
├── docs/
│   ├── README.md              # This file
│   ├── DEPLOY.md              # Deployment guide
│   └── OTP_SETUP.md           # OTP provider configuration
│
└── tests/                     # Unit, integration & verification scripts
    ├── test_app.py
    ├── test_engine.py
    ├── verify_*.py
    └── ...
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- PowerShell (Windows) or Terminal (macOS/Linux)

### 2. Virtual Environment Setup

Clone or navigate into the project directory:
```powershell
cd AP_ECET_Counselling_Forecasting_System
```

Activate the virtual environment:
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

If setting up fresh dependencies:
```powershell
pip install -r requirements.txt
```

### 3. Initialize the Database
The database tables and indexes are initialized automatically on app startup, or manually:
```powershell
python -c "from database import init_db; init_db()"
```

### 4. Run the Development Server
```powershell
python app.py
```
The application will start on:
👉 **`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

Run the test suites with virtualenv Python to verify all routing, role guards, and UI logic:

```powershell
# Verify Architecture, Landing Page, SVG Toggles, Separate Logins & Profile Flow
python -m unittest tests.verify_landing_page   # or: PYTHONPATH=. python tests/verify_landing_page.py

# Verify Full System Features (Forecasting, What-If, Preferences, PDF Export, Reports)
python -m unittest tests.test_app   # or: PYTHONPATH=. python tests/test_app.py
```

---

## 🔒 Security & Role Guard Implementation

- **Candidate vs. Admin Isolation**:
  - Candidate authentication route: `/login`
  - Administrator authentication route: `/admin/login`
  - Attempting to log into the Administrator Portal with student credentials triggers a **Role Guard** rejection and redirects to `/login`.
  - Unauthenticated access to protected student pages (`/dashboard`, `/profile`, `/predict`, etc.) prompts a modal sign-in or redirects to `/login`.
  - Administrator pages (`/admin/*`) require explicit `admin` role authorization; unauthorized sessions redirect to `/admin/login`.
- **Password Security**: Passwords are cryptographically hashed using PBKDF2 with SHA-256 via Werkzeug.
- **Client-Side Toggle**: Password show/hide functionality uses clean vector SVGs without external emoji dependencies.

---

## 📄 License & Attribution

Designed and developed for AP ECET (Andhra Pradesh Engineering Common Entrance Test) lateral entry counseling preparation.
Data reference: APSCHE & Department of Technical Education, Government of Andhra Pradesh.
