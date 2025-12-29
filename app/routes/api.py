from __future__ import annotations

import logging
from flask import Blueprint, jsonify

from app.services.provider import DataProvider
from app.services.scoring import compute_player_score, detect_scenario, scenario_weights
from app.services.optimizer import select_squad

api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


@api_bp.get("/health")
def health():
	"""Simple health check that doesn't depend on external services"""
	return jsonify({"status": "ok", "message": "FPL AI API is running"}), 200


@api_bp.get("/generate")
def generate_squad():
	"""Generate optimal FPL squad for current gameweek"""
	try:
		logger.info("Starting squad generation...")
		provider = DataProvider()
		players, gw, deadline, meta = provider.load_players_for_current_gw()

		is_double = meta.get("double_gw") == "True"
		is_blank = meta.get("blank_gw") == "True"
		# Naive end-season heuristic: last 6 events id >= 33 (FPL has 38)
		is_end_season = bool(gw and gw >= 33)
		is_wildcard_week = False  # placeholder (could be parameterized)

		scenario = detect_scenario(
			is_double=is_double, is_blank=is_blank, is_end_season=is_end_season, is_wildcard_week=is_wildcard_week
		)
		w = scenario_weights(scenario)

		scored = [(p, compute_player_score(p, w)) for p in players]
		scored.sort(key=lambda t: t[1], reverse=True)

		squad = select_squad(scored, gameweek=gw or 0, deadline=deadline)
		
		logger.info(f"Squad generated successfully for GW{gw}")

		return jsonify({
			"gameweek": squad.gameweek,
			"deadline": squad.deadline,
			"budget_used": squad.budget_used,
			"budget_limit": squad.budget_limit,
			"captain": squad.captain_id,
			"vice_captain": squad.vice_captain_id,
			"starting": [
				{
					"id": sm.player.id,
					"name": sm.player.name,
					"team": sm.player.team_name,
					"pos": sm.player.position,
					"price": sm.player.price,
					"pred": sm.player.predicted_points,
				}
				for sm in squad.starting
			],
			"bench": [
				{
					"id": sm.player.id,
					"name": sm.player.name,
					"team": sm.player.team_name,
					"pos": sm.player.position,
					"price": sm.player.price,
					"pred": sm.player.predicted_points,
				}
				for sm in squad.bench
			],
			"meta": {"formation": squad.metadata.get("formation"), "scenario": scenario},
		}), 200
	except Exception as e:
		logger.error(f"Error generating squad: {str(e)}", exc_info=True)
		return jsonify({
			"error": "Failed to generate squad",
			"message": str(e),
			"status": "error"
		}), 500


@api_bp.get("/reshuffle")
def reshuffle_squad():
	"""Generate alternative squad variant with differential bias"""
	try:
		logger.info("Starting squad reshuffle...")
		provider = DataProvider()
		players, gw, deadline, meta = provider.load_players_for_current_gw()

		is_double = meta.get("double_gw") == "True"
		is_blank = meta.get("blank_gw") == "True"
		is_end_season = bool(gw and gw >= 33)

		# Reshuffle biases towards differentials: reduce value weight, increase form
		w = scenario_weights(
			detect_scenario(is_double=is_double, is_blank=is_blank, is_end_season=is_end_season, is_wildcard_week=False)
		)
		w = w.model_copy(update={"form": min(0.25, w.form + 0.10), "value_per_million": max(0.0, w.value_per_million - 0.05)})

		scored = [(p, compute_player_score(p, w)) for p in players]
		scored.sort(key=lambda t: t[1], reverse=True)
		squad = select_squad(scored, gameweek=gw or 0, deadline=deadline)
		
		logger.info(f"Reshuffle completed for GW{gw}")
		
		return jsonify({
			"variant": "differential",
			"gameweek": squad.gameweek,
			"starting_count": len(squad.starting),
			"bench_count": len(squad.bench),
			"captain": squad.captain_id,
			"starting": [sm.player.name for sm in squad.starting],
			"bench": [sm.player.name for sm in squad.bench],
		}), 200
	except Exception as e:
		logger.error(f"Error reshuffling squad: {str(e)}", exc_info=True)
		return jsonify({
			"error": "Failed to reshuffle squad",
			"message": str(e),
			"status": "error"
		}), 500
