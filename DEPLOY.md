# Deploying to Railway

## What gets deployed

This project exposes a **FastAPI backend** (`main.py → api/app.py`).
The Streamlit UI can be deployed as a **separate Railway service** pointing at the API URL.

---

## Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/multi-ai-customer-support.git
git push -u origin main
```

---

## Step 2 — Create Railway project

1. Go to [railway.app](https://railway.app) → **New Project**
2. Choose **Deploy from GitHub repo**
3. Select your repository

Railway will detect `nixpacks.toml` and `Procfile` automatically.

---

## Step 3 — Set environment variables

In Railway dashboard → your service → **Variables**, add:

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | `sk-...` your OpenAI key |
| `PORT` | Railway sets this automatically — **do not set manually** |

---

## Step 4 — Add the FAISS index (two options)

### Option A — Pre-built index (recommended)
Run ingestion locally first, then commit the index:

```bash
python -m rag.ingest          # builds data/faiss_index/
git add data/faiss_index/
git commit -m "add faiss index"
git push
```

### Option B — Build during deploy
The `nixpacks.toml` build phase runs `python -m rag.ingest` automatically,
but **the PDF files must be committed** to the repo for this to work:

```bash
git add data/*.pdf
git commit -m "add knowledge base PDFs"
git push
```

---

## Step 5 — Verify deployment

Once deployed, Railway gives you a public URL like:
`https://your-app-name.up.railway.app`

Test it:
```bash
curl https://your-app-name.up.railway.app/api/v1/health
```

Expected response:
```json
{"status":"ok","version":"1.0.0","vector_store":"ok","database":"ok"}
```

Swagger UI: `https://your-app-name.up.railway.app/docs`

---

## Step 6 — Deploy Streamlit UI (optional second service)

1. In Railway → **New Service** → **GitHub repo** (same repo)
2. Override the start command to:
   ```
   streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```
3. Add variable:
   ```
   API_BASE_URL = https://your-fastapi-service.up.railway.app/api/v1
   ```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Could not import module "main"` | Ensure `main.py` is committed at the repo root |
| `OPENAI_API_KEY is not set` | Add it in Railway → Variables |
| `FAISS index not found` | Either commit `data/faiss_index/` or commit PDFs and let nixpacks build it |
| `Port already in use` | Railway always injects `$PORT` — never hardcode 8000 in the start command |
| Health check failing | Check `/api/v1/health` endpoint returns 200; increase `healthcheckTimeout` in `railway.toml` |
