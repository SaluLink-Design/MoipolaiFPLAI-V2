# AI FPL Squad Generator

A Flask app that generates optimal Fantasy Premier League squads for each gameweek using live FPL data, dynamic weighted scoring, and a greedy optimizer that respects FPL constraints.

## Quickstart

1. Python 3.11+ recommended
2. Create venv and install deps:
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run:
   
   ```bash
   python wsgi.py
   ```
4. Open `http://localhost:5000` and click Generate Squad.

## Features
- Dynamic weights per scenario (default, double, blank, wildcard, end-season)
- Live data from FPL `bootstrap-static`, `fixtures`, `event-status`
- Greedy optimizer enforcing budget 100.0, 2 GKP / 5 DEF / 5 MID / 3 FWD, max 3 per club
- Reshuffle variants bias towards differentials

## API
- `GET /api/health` – health check
- `GET /api/generate` – returns 15-man squad, metadata, captain/vice
- `GET /api/reshuffle` – returns alternative squad variant

## Structure
- `app/routes/` – `views` (HTML) and `api` (JSON)
- `app/services/` – `fpl_client.py`, `provider.py`, `scoring.py`, `optimizer.py`
- `app/models/` – Pydantic schemas

## Notes
- Predictions currently use FPL `ep_next` as a proxy. You can swap in third-party xG/xA model outputs in `provider.py`.
- Deadline awareness: the client exposes deadline time; further locking logic can be added in routes using `FplClient.is_after_deadline()`.
