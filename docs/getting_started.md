# Getting Started

Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Frontend

```bash
cd frontend
npm install
npm run dev
```

Using Docker Compose

```bash
docker compose up --build
```
