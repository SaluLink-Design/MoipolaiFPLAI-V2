from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List, Tuple

import requests

BOOTSTRAP_STATIC = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"
EVENTS = "https://fantasy.premierleague.com/api/event-status/"


class FplClient:
	def __init__(self, session: requests.Session | None = None) -> None:
		self.session = session or requests.Session()

	def get_bootstrap(self) -> Dict[str, Any]:
		resp = self.session.get(BOOTSTRAP_STATIC, timeout=20)
		resp.raise_for_status()
		return resp.json()

	def get_fixtures(self) -> List[Dict[str, Any]]:
		resp = self.session.get(FIXTURES, timeout=20)
		resp.raise_for_status()
		return resp.json()

	def get_event_status(self) -> Dict[str, Any]:
		resp = self.session.get(EVENTS, timeout=20)
		resp.raise_for_status()
		return resp.json()

	def get_current_gameweek_and_deadline(self) -> Tuple[int | None, str | None]:
		data = self.get_bootstrap()
		for event in data.get("events", []):
			if event.get("is_current"):
				deadline = event.get("deadline_time")
				return event.get("id"), deadline
		return None, None

	def is_after_deadline(self) -> bool:
		_, deadline = self.get_current_gameweek_and_deadline()
		if not deadline:
			return False
		# Compare in UTC
		try:
			dt_deadline = dt.datetime.fromisoformat(deadline.replace("Z", "+00:00"))
			return dt.datetime.now(dt.timezone.utc) >= dt_deadline
		except Exception:
			return False
