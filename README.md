# Earth Watch — Illegal Mine Detection System

AI-powered geospatial system for detecting illegal mines using Sentinel-2 satellite imagery, a ResNet34+UNet dual-head model, and PostGIS legal classification.

---

## Project Structure

```
Earth_watch/
├── api.py                          ← FastAPI entry point
├── mine_detection.py               ← GEE + inference pipeline
├── setup_legal_mines.py            ← One-time DB setup
├── requirements.txt
├── .env                            ← Your secrets (gitignored)
├── .env.example                    ← Template to copy
│
├── backend/
│   ├── config.py                   ← All settings (reads .env)
│   ├── routers/
│   │   ├── detect.py               ← POST /api/detect
│   │   └── verify.py               ← GET/POST /api/verified /api/verify
│   └── utils/
│       ├── db.py                   ← DB connection helpers
│       └── thumbnail.py            ← Sentinel-2 thumbnail generator
│
├── clean_data_model/
│   └── best_model.pt               ← Trained model weights (not in git)
│
└── frontend/                       ← Next.js app
    ├── .env.local                  ← NEXT_PUBLIC_API_URL (gitignored)
    └── src/app/dashboard/page.tsx  ← Main dashboard
```

---

## Setup

### 1. Clone and enter directory
```bash
cd Earth_watch
```

### 2. Create virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your Supabase password, GEE project, etc.
```

### 5. Authenticate Google Earth Engine (first time only)
```bash
earthengine authenticate
```

### 6. Set up the legal mines database (first time only)
```bash
python setup_legal_mines.py
```
This loads the Maus et al. 2022 global mining polygons into your Supabase PostGIS table.

### 7. Place your trained model
```
clean_data_model/best_model.pt
```

---

## Running the Backend

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

---

## Running the Frontend

```bash
cd frontend
npm install          # First time only
npm run dev
```

Frontend runs at `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint         | Description                              |
|--------|-----------------|------------------------------------------|
| GET    | `/`             | Health check                             |
| GET    | `/ping`         | Ping                                     |
| POST   | `/api/detect`   | Run mine detection on a GeoJSON polygon  |
| GET    | `/api/verified` | List all officer-verified mines          |
| POST   | `/api/verify`   | Mark a mine as verified (USER_LEGAL)     |

### POST /api/detect — Request body
```json
{
  "geojson": {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[lon, lat], ...]]
    }
  }
}
```

---

## Errors Fixed

| Error | Cause | Fix |
|-------|-------|-----|
| `data-fill layer does not exist` | `queryRenderedFeatures` called before layer is added to map | Wrapped in `if (geoData && !loading)` guard |
| `Axios 500 on /api/detect` | Hardcoded DB credentials, monolithic api.py | Moved all config to `.env` + `backend/config.py` |
| `THREE.Clock deprecated` | Old Three.js API in EarthGlobe.tsx | Cosmetic warning only — use `THREE.Timer` if you update that component |
| Hardcoded `window.location.hostname:8000` | Not portable across environments | Replaced with `NEXT_PUBLIC_API_URL` env var |

---

## Environment Variables Reference

| Variable | Used by | Description |
|----------|---------|-------------|
| `PGDATABASE` | FastAPI | Supabase DB name |
| `PGUSER` | FastAPI | Supabase pooler user |
| `PGPASSWORD` | FastAPI | Supabase password |
| `PGHOST` | FastAPI | Supabase pooler host |
| `PGPORT` | FastAPI | Supabase pooler port (6543) |
| `DB_DIRECT_USER` | mine_detection | Direct DB user |
| `DB_DIRECT_PASSWORD` | mine_detection | Direct DB password |
| `DB_DIRECT_HOST` | mine_detection | Direct DB host |
| `DB_DIRECT_PORT` | mine_detection | Direct DB port (5432) |
| `GEE_PROJECT` | mine_detection | GEE project ID |
| `MODEL_PATH` | mine_detection | Path to .pt weights file |
| `API_HOST` | uvicorn | Bind host (default 0.0.0.0) |
| `API_PORT` | uvicorn | Bind port (default 8000) |
| `NEXT_PUBLIC_API_URL` | Next.js | Backend URL for frontend |
