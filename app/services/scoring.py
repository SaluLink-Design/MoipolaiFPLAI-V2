from __future__ import annotations

from typing import Literal

from app.models.schemas import Player, Weights

Scenario = Literal[
	"default",
	"double",
	"blank",
	"wildcard",
	"end_season",
]


def scenario_weights(scenario: Scenario) -> Weights:
	if scenario == "double":
		return Weights(
			predicted_points=0.45,
			fixture_difficulty=0.30,
			rotation_minutes=0.20,
			value_per_million=0.05,
			form=0.0,
		)
	if scenario == "blank":
		return Weights(
			predicted_points=0.35,
			rotation_minutes=0.25,
			fixture_difficulty=0.20,
			value_per_million=0.15,
			form=0.05,
		)
	if scenario == "wildcard":
		return Weights(
			predicted_points=0.40,
			fixture_difficulty=0.30,
			form=0.15,
			rotation_minutes=0.10,
			value_per_million=0.05,
		)
	if scenario == "end_season":
		return Weights(
			predicted_points=0.40,
			form=0.20,
			fixture_difficulty=0.20,
			rotation_minutes=0.15,
			value_per_million=0.05,
		)
	return Weights(
		predicted_points=0.40,
		fixture_difficulty=0.25,
		value_per_million=0.10,
		rotation_minutes=0.15,
		form=0.10,
	)


def detect_scenario(*, is_double: bool, is_blank: bool, is_end_season: bool, is_wildcard_week: bool) -> Scenario:
	if is_wildcard_week:
		return "wildcard"
	if is_double:
		return "double"
	if is_blank:
		return "blank"
	if is_end_season:
		return "end_season"
	return "default"


def compute_player_score(player: Player, weights: Weights) -> float:
	vpm = player.predicted_points / max(player.price, 0.1)
	fixture_component = (5.0 - player.fixture_difficulty)  # invert so easier fixtures score higher
	rotation_component = player.minutes_avg90 / 90.0
	return (
		weights.predicted_points * player.predicted_points
		+ weights.fixture_difficulty * fixture_component
		+ weights.value_per_million * vpm
		+ weights.rotation_minutes * rotation_component
		+ weights.form * player.form
	)
