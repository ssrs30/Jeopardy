from __future__ import annotations
from typing import Any


class ClueOutcomeResolver:
    """Apply the outcome of the first player/AI"""

    def __init__(self, game: Any) -> None:
        self._g = game

    def get_payload(self) -> dict:
        """Return the question dict to game.selected_pos"""
        row, col = self._g.selected_pos
        return self._g.question_list[f"round{self._g.round_no}"][col]["questions"][row]

    def resolve_first_responder(self, winner: str, is_correct: bool) -> None:
        """Apply score and stats for the first responder, clear wager anditem"""
        q = self.get_payload()
        base_value = int(q.get("value", 0))
        options = q.get("options", [])
        correct_idx = int(q.get("correct", 0))
        correct_answer_text = ""
        if isinstance(options, list) and 0 <= correct_idx < len(options):
            correct_answer_text = str(options[correct_idx])
        clue_value = self._g.current_question_wager if self._g.current_question_is_daily_double else base_value
        if winner == "human":
            if is_correct:
                self._g.human_correct_clues += 1
                awarded = clue_value * 2 if self._g.human_double_active else clue_value
                self._g.player_score += awarded
                self._g.result_window.update_result(self._g.player_name, awarded, True)
            else:
                if self._g.human_shield_active:
                    self._g.result_window.update_custom_message("Shield active! No penalty this question.", "-0")
                else:
                    self._g.player_score -= clue_value
                    self._g.result_window.update_result(self._g.player_name, clue_value, False)
        elif winner == "ai_1":
            if is_correct:
                self._g.ai_players[0].correct_clues += 1
                self._g.ai_players[0].add_score(clue_value)
            else:
                self._g.ai_players[0].subtract_score(clue_value)
            self._g.result_window.update_result(
                self._g.ai_players[0].name, clue_value, is_correct, play_feedback_sound=False
            )
        elif winner == "ai_2":
            if is_correct:
                self._g.ai_players[1].correct_clues += 1
                self._g.ai_players[1].add_score(clue_value)
            else:
                self._g.ai_players[1].subtract_score(clue_value)
            self._g.result_window.update_result(
                self._g.ai_players[1].name, clue_value, is_correct, play_feedback_sound=False
            )
        if not is_correct or winner in ("ai_1", "ai_2"):
            self._g.result_window.set_correct_answer(correct_answer_text)
        self._g._sync_ai_scores()
        for ai in self._g.ai_players:
            ai.cancel_pending()
        self._g.current_question_is_daily_double = False
        self._g.current_question_wager = 0
        self._g.active_human_item = 0
        self._g.human_double_active = False
        self._g.human_shield_active = False
