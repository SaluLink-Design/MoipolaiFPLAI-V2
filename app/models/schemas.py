from __future__ import annotations

from typing import List, Optional, Dict
from pydantic import BaseModel


class Weights(BaseModel):
	predicted_points: float
	fixture_difficulty: float
	value_per_million: float
	rotation_minutes: float
	form: float


class Player(BaseModel):
	id: int
	name: str
	team_id: int
	team_name: str
	position: str  # GKP, DEF, MID, FWD
	price: float  # in millions
	form: float
	minutes_avg90: float
	predicted_points: float
	fixture_difficulty: float  # lower is easier; we will invert when scoring
	selected_by_percent: float


class SquadMember(BaseModel):
	player: Player
	is_starting: bool


class Squad(BaseModel):
	gameweek: int
	deadline: Optional[str]
	budget_used: float
	budget_limit: float
	captain_id: Optional[int]
	vice_captain_id: Optional[int]
	starting: List[SquadMember]
	bench: List[SquadMember]
	metadata: Dict[str, str] = {}
