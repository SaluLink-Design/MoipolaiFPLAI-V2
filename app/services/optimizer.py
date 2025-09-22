from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from app.models.schemas import Player, Squad, SquadMember

BUDGET_LIMIT = 100.0
SQUAD_STRUCTURE = {"GKP": 2, "DEF": 5, "MID": 5, "FWD": 3}
MAX_PER_CLUB = 3


def select_squad(sorted_players: List[Tuple[Player, float]], gameweek: int, deadline: str | None) -> Squad:
	selected: List[Player] = []
	club_counts: Dict[int, int] = defaultdict(int)
	position_counts: Dict[str, int] = defaultdict(int)
	budget_used = 0.0

	for player, score in sorted_players:
		if position_counts[player.position] >= SQUAD_STRUCTURE.get(player.position, 0):
			continue
		if club_counts[player.team_id] >= MAX_PER_CLUB:
			continue
		if budget_used + player.price > BUDGET_LIMIT:
			continue
		selected.append(player)
		club_counts[player.team_id] += 1
		position_counts[player.position] += 1
		budget_used += player.price
		if len(selected) == 15:
			break

	# Basic 11 starters: 1-3-4-3 (common)
	starting: List[SquadMember] = []
	bench: List[SquadMember] = []
	counts = {"GKP": 0, "DEF": 0, "MID": 0, "FWD": 0}
	for p in selected:
		if p.position == "GKP" and counts["GKP"] < 1:
			starting.append(SquadMember(player=p, is_starting=True))
			counts["GKP"] += 1
		elif p.position == "DEF" and counts["DEF"] < 3:
			starting.append(SquadMember(player=p, is_starting=True))
			counts["DEF"] += 1
		elif p.position == "MID" and counts["MID"] < 4:
			starting.append(SquadMember(player=p, is_starting=True))
			counts["MID"] += 1
		elif p.position == "FWD" and counts["FWD"] < 3:
			starting.append(SquadMember(player=p, is_starting=True))
			counts["FWD"] += 1
		else:
			bench.append(SquadMember(player=p, is_starting=False))

	# Captain = highest predicted points among starters
	if starting:
		captain = max(starting, key=lambda sm: sm.player.predicted_points).player.id
		vc = max(
			[start for start in starting if start.player.id != captain] or starting,
			key=lambda sm: sm.player.predicted_points,
		).player.id
	else:
		captain = None
		vc = None

	return Squad(
		gameweek=gameweek or 0,
		deadline=deadline,
		budget_used=round(budget_used, 1),
		budget_limit=BUDGET_LIMIT,
		captain_id=captain,
		vice_captain_id=vc,
		starting=starting,
		bench=bench,
		metadata={"formation": "1-3-4-3", "note": "Greedy selection"},
	)
