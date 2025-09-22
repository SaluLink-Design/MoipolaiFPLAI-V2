from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from app.models.schemas import Player
from app.services.fpl_client import FplClient

POSITION_MAP = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}


class DataProvider:
	def __init__(self, client: FplClient | None = None) -> None:
		self.client = client or FplClient()

	def load_players_for_current_gw(self) -> Tuple[List[Player], int | None, str | None, Dict]:
		bootstrap = self.client.get_bootstrap()
		fixtures = self.client.get_fixtures()
		gw, deadline = self.client.get_current_gameweek_and_deadline()

		teams_map = {t["id"]: t for t in bootstrap.get("teams", [])}

		# Build fixture difficulty per team for current gw (average of opponent strength)
		fixture_difficulty_by_team: Dict[int, float] = defaultdict(lambda: 3.0)
		matches_this_gw = [f for f in fixtures if gw and f.get("event") == gw]
		opponents: Dict[int, List[float]] = defaultdict(list)
		for fx in matches_this_gw:
			h = fx.get("team_h")
			a = fx.get("team_a")
			if not h or not a:
				continue
			# Use opponent strength (1-5-ish using 'strength') and normalize to 1-5
			h_opp_strength = float(teams_map.get(a, {}).get("strength", 3))
			a_opp_strength = float(teams_map.get(h, {}).get("strength", 3))
			# Convert strength (~1300-1800) to 1-5 scale roughly
			def map_strength(s: float) -> float:
				return 1.0 + 4.0 * (max(1000.0, min(2000.0, s)) - 1000.0) / 1000.0
			opponents[h].append(map_strength(a_opp_strength))
			opponents[a].append(map_strength(h_opp_strength))
		for team_id, vals in opponents.items():
			fixture_difficulty_by_team[team_id] = sum(vals) / max(1, len(vals))

		players: List[Player] = []
		teams_name_map = {t["id"]: t["name"] for t in bootstrap.get("teams", [])}
		for e in bootstrap.get("elements", []):
			team_id = e.get("team")
			position = POSITION_MAP.get(e.get("element_type"), "MID")
			price = float(e.get("now_cost", 0)) / 10.0
			form = float(e.get("form") or 0.0)
			minutes = float(e.get("minutes") or 0.0)
			appearances = max(1.0, float(e.get("starts") or e.get("appearances", 1.0)))
			minutes_avg90 = min(90.0, minutes / appearances) if appearances else 0.0
			# Use FPL's ep_next if present as predicted points proxy
			pred_points = float(e.get("ep_next") or e.get("ep_this") or 0.0)
			selected_by = float((e.get("selected_by_percent") or "0").replace("%", ""))
			fixture_diff = float(fixture_difficulty_by_team.get(team_id, 3.0))
			players.append(
				Player(
					id=int(e["id"]),
					name=f"{e.get('first_name','')} {e.get('second_name','')}".strip(),
					team_id=int(team_id or 0),
					team_name=teams_name_map.get(int(team_id or 0), "Unknown"),
					position=position,
					price=price,
					form=form,
					minutes_avg90=minutes_avg90,
					predicted_points=pred_points,
					fixture_difficulty=fixture_diff,
					selected_by_percent=selected_by,
				)
			)

		metadata = {
			"double_gw": str(any(len(v) > 1 for v in opponents.values())),
			"blank_gw": str(any(len(v) == 0 for v in opponents.values())),
		}
		return players, gw, deadline, metadata
