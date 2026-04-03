# 🌍 Earth Watch — AI-Powered Geospatial Analysis Platform

Earth Watch is a full-stack geospatial intelligence platform that uses satellite imagery, deep learning, and cloud-native GIS to detect **illegal mines**, analyze **land use**, monitor **deforestation**, map **landslide risk**, detect **buildings**, track **forest fires**, and measure **snow cover** — all from a single interactive dashboard.

---

## ✨ Features

| Analysis | Method | Data Source |
|----------|--------|-------------|
| 🪨 **Illegal Mine Detection** | ResNet34 + UNet (PyTorch) | Sentinel-2 (10 m) via GEE |
| 🏘️ **Building Detection** | Custom U-Net (TensorFlow) | Sentinel-2 + Google Open Buildings |
| 🌱 **Land Use / Land Cover** | 1D-CNN (TensorFlow) | Google Dynamic World (10 m) |
| ⛰️ **Landslide Susceptibility** | Random Forest + Deep Learning | NASA NASADEM (90 m) |
| 🔥 **Forest Fire Burn Severity** | dNBR Index | Sentinel-2 via GEE |
| ❄️ **Snow Cover Mapping** | NDSI Index | Sentinel-2 via GEE |
| 🌲 **Deforestation Detection** | Forest cover change analysis | Sentinel-2 via GEE |
| ✅ **Officer Verification** | PostGIS + Supabase | User-verified mine table |

---

## 🏗️ Architecture

```
Earth-Watch/
├── api.py                          ← FastAPI entry point
├── requirements.txt                ← Python dependencies
├── .env.example                    ← Environment variable template
│
├── backend/
│   ├── config.py                   ← Centralized settings (reads .env)
│   ├── controllers/                ← REST API route handlers
│   │   ├── detect.py               ← Mine detection endpoint
│   │   ├── verify.py               ← Officer verification endpoints
│   │   ├── lulc.py                 ← Land Use/Cover endpoint
│   │   ├── building.py             ← Building detection endpoint
│   │   ├── landslide.py            ← Landslide susceptibility endpoint
│   │   ├── fire.py                 ← Forest fire endpoint
│   │   ├── snow.py                 ← Snow cover endpoint
│   │   └── deforestation.py        ← Deforestation endpoint
│   ├── ml_models/                  ← Trained model weights (*.pt, *.h5)
│   ├── services/
│   │   └── analysis/               ← Core AI inference and GEE pipelines
│   └── utils/                      ← Database helpers, thumbnail generation
│
├── data/                           ← Global GeoPackages and sample data
│   └── training_data/              ← GEE tile buffers for ML training
│
├── frontend/                       ← Next.js interactive dashboard
│
├── ml_training/                    ← Standalone model training scripts
│
└── scripts/                        ← Developer testing notebooks
```

---

## 🤖 ML Models

| Model | Framework | Architecture | Input | Purpose |
|-------|-----------|-------------|-------|---------|
| `best_model.pt` | PyTorch | ResNet34 + UNet | 11-band Sentinel-2, 512×512 px | Mine detection segmentation |
| `custom_building_best.h5` | TensorFlow/Keras | U-Net | Sentinel-2 patches | Building footprint segmentation |
| `custom_landslide_best.h5` | TensorFlow/Keras | U-Net | DEM terrain variables | Landslide susceptibility mapping |
| `lulc_custom_model.h5` | TensorFlow/Keras | 1D-CNN | 10 spectral channels | Land use classification (9 classes) |

### Mine Detection Pipeline

1. **Tiling** — AOI is split into 5×5 km overlapping tiles (50% overlap)
2. **GEE Retrieval** — Sentinel-2 composites downloaded and cloud-masked (6-month window)
3. **Inference** — PyTorch ResNet34+UNet produces pixel-level mine probability masks
4. **Merging** — Overlapping detections merged using IoU threshold (0.15)
5. **Legal Classification** — PostGIS cross-reference against Maus et al. 2022 global mining polygons:
   - 🔴 **ILLEGAL** — No overlap with known legal polygon (IoU ≤ 0.10)
   - 🟡 **SUSPECT** — Partial overlap (0.10 < IoU ≤ 0.30)
   - 🟢 **LEGAL** — Significant overlap (IoU > 0.30)
6. **Thumbnails** — 400×400 base64-encoded preview images with confidence overlays

---

## 🖥️ Tech Stack

### Backend
- **FastAPI** + **Uvicorn** — REST API server
- **PyTorch 2.0+** — Primary mine detection model (CUDA / MPS / CPU)
- **TensorFlow 2.10+** — Building, landslide, and LULC models
- **Google Earth Engine API** — Satellite data retrieval and processing
- **Rasterio / GeoPandas / Shapely** — Geospatial data processing
- **Supabase PostgreSQL + PostGIS** — Spatial database for legal mine polygons and officer verification
- **Diskcache** — Tile-level GEE caching (180-day validity)

### Frontend
- **Next.js 16** (React 19) — Interactive dashboard
- **MapLibre GL** — Vector map rendering
- **Mapbox GL Draw** — Draw polygons and rectangles on the map
- **Three.js + React Globe GL** — 3D Earth globe visualization
- **Tailwind CSS 4** — UI styling
- **Framer Motion** — Page and component animations
- **Axios** — Backend API communication

---

## 🚀 Setup

### 1. Clone and enter the directory
```bash
git clone https://github.com/Harsh-Atkare/Earth-Watch.git
cd Earth-Watch
```

### 2. Create a Python virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in the following keys:

| Variable | Description |
|----------|-------------|
| `PGDATABASE` | Supabase database name |
| `PGUSER` | Supabase pooler username |
| `PGPASSWORD` | Supabase database password |
| `PGHOST` | Supabase pooler host |
| `PGPORT` | Supabase pooler port (default: `6543`) |
| `DB_DIRECT_USER` | Supabase direct connection user |
| `DB_DIRECT_PASSWORD` | Supabase direct connection password |
| `DB_DIRECT_HOST` | Supabase direct connection host |
| `DB_DIRECT_PORT` | Supabase direct connection port (default: `5432`) |
| `GEE_PROJECT` | Google Earth Engine project ID (see below) |
| `MODEL_PATH` | Path to the `.pt` model weights file |
| `NEXT_PUBLIC_API_URL` | Backend URL for the frontend (default: `http://localhost:8000`) |
| `API_HOST` | Uvicorn bind host (default: `0.0.0.0`) |
| `API_PORT` | Uvicorn bind port (default: `8000`) |

---

### 5. Get a Google Earth Engine Project ID (Non-Commercial Access)

Google Earth Engine is free for non-commercial and research use.

**Step 1 — Sign up for GEE access**
1. Go to [https://earthengine.google.com](https://earthengine.google.com) and click **Sign Up**.
2. Sign in with a Google account.
3. Fill in the registration form. Under **Use Case**, select **Research / Non-Commercial**.
4. Submit and wait for approval (usually a few minutes to a few hours).

**Step 2 — Create a Cloud Project**
1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Click **Select a project** → **New Project**.
3. Name the project (e.g., `earth-watch-gee`) and click **Create**.
4. Note the **Project ID** shown under the project name — this is your `GEE_PROJECT` value.
5. Go to **APIs & Services → Library**, search for **Earth Engine API**, and click **Enable**.

**Step 3 — Register your project with Earth Engine**
1. Go to [https://code.earthengine.google.com](https://code.earthengine.google.com).
2. Click your avatar → **Register a new cloud project**.
3. Select the Cloud project you created and register it for **Non-Commercial / Research** use.

**Step 4 — Add your Project ID to `.env`**
```
GEE_PROJECT=your-project-id-here
```

---

### 6. Authenticate Google Earth Engine

Run this once to authorize your machine:

```bash
earthengine authenticate
```

This opens a browser window to log in with the Google account linked to your GEE project. The credentials token is saved locally and reused automatically.

> **Remote server (no browser)?** Use:
> ```bash
> earthengine authenticate --quiet
> ```
> and follow the link printed in the terminal.

---

### 7. Set up the legal mines database

Load the Maus et al. 2022 global mining polygons into your Supabase PostGIS table (run once):

```bash
python ml_training/setup_legal_mines.py
```

This creates the `legal_mines` table, inserts all global mining polygons, and builds a spatial index for fast intersection queries.

### 8. Place trained model weights

```
backend/ml_models/best_model.pt
backend/ml_models/custom_building_best.h5
backend/ml_models/custom_landslide_best.h5
backend/ml_models/lulc_custom_model.h5
```

---

## ▶️ Running the App

### Backend
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install          # First time only
npm run dev
```

- Dashboard: `http://localhost:3000`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/ping` | Ping |
| POST | `/api/detect` | Run mine detection on a GeoJSON polygon |
| GET | `/api/verified` | List all officer-verified mines |
| POST | `/api/verify` | Mark a mine as verified (USER_LEGAL) |
| POST | `/api/lulc` | Land Use / Land Cover classification |
| POST | `/api/building` | Building / built-up area detection |
| POST | `/api/landslide` | Landslide susceptibility analysis |
| POST | `/api/fire` | Forest fire burn severity (dNBR) |
| POST | `/api/snow` | Snow cover mapping (NDSI) |
| POST | `/api/deforestation` | Deforestation / forest cover change |

### Example: POST `/api/detect`
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

**Response** includes GeoJSON features with:
- `verdict`: `ILLEGAL` | `SUSPECT` | `LEGAL` | `USER_LEGAL`
- `confidence`: model confidence score (0–1)
- `area_km2`: detected mine area in km²
- `thumbnail`: base64-encoded 400×400 PNG preview

---

## 🗄️ Database Schema

| Table | Description |
|-------|-------------|
| `legal_mines` | Global mining polygons from Maus et al. 2022 (PostGIS geometry + spatial index) |
| `user_verified_mines` | Officer-verified mines with `mine_id`, `geom`, `area_km2`, `reason`, `notes`, `created_at` |

---

## 🧠 Training Your Own Models

Training scripts are in `ml_training/`:

| Script | Purpose |
|--------|---------|
| `train_custom_building.py` | Train U-Net for building detection on GEE-extracted data |
| `train_custom_landslide.py` | Train U-Net for landslide susceptibility |
| `lulc_trainer.py` | Train 1D-CNN for LULC classification (10 spectral bands → 9 classes) |
| `setup_legal_mines.py` | Load Maus et al. 2022 mining polygons into Supabase |
| `showcase_lulc.py` | Visualize LULC predictions as a color map |
| `test_landslide.py` | Test the landslide model on a sample AOI |

Training data lives in `data/training_data/`:
- `building_training_data/processed/` — Sentinel-2 patches with building labels
- `landslide_training_data/` — DEM terrain variables with landslide labels
- `lulc_training_data/samples/lulc_samples.csv` — Spectral samples with class labels

---

## ⚙️ Configuration Reference

Key settings in `backend/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `TILE_KM` | `5.0` | Tile size in kilometers |
| `OVERLAP_FRAC` | `0.5` | Tile overlap fraction (50%) |
| `TARGET_SIZE` | `512` | Model input size (pixels) |
| `SCALE` | `10` | Sentinel-2 pixel resolution (metres) |
| `CLOUD_THRESH` | `20` | Max cloud coverage % |
| `COMP_MONTHS` | `6` | Composite window (months) |
| `SEG_THRESHOLD` | `0.50` | Segmentation confidence threshold |
| `MINE_THRESHOLD` | `0.50` | Mine detection confidence threshold |
| `IOU_MERGE_THRESH` | `0.15` | IoU threshold for merging overlapping detections |
| `IOU_LEGAL_THRESH` | `0.30` | Minimum IoU overlap for LEGAL verdict |
| `IOU_SUSPECT_THRESH` | `0.10` | Minimum IoU overlap for SUSPECT verdict |
| `CACHE_VALID_DAYS` | `180` | GEE tile cache validity (days) |
| `N_CHANNELS` | `11` | Number of Sentinel-2 input channels |
| `S2_BANDS` | B2–B12 | Sentinel-2 band selection |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source. See [LICENSE](LICENSE) for details.

---

## 📚 References

- Maus, V., et al. (2022). *Global-scale mining polygons (Version 2)*. PANGAEA. [https://doi.org/10.1594/PANGAEA.942325](https://doi.org/10.1594/PANGAEA.942325)
- Google Earth Engine: [https://earthengine.google.com](https://earthengine.google.com)
- Sentinel-2 (ESA Copernicus): [https://sentinel.esa.int](https://sentinel.esa.int)