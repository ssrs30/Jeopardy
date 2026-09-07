import json
import random
import sys
import threading
from pathlib import Path

import pygame

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import LLM
from contestants import AIPlayer
from offline_questions import is_valid_question_pack, load_offline_questions
from UI import board, char, daily_double, game_over, get_ready, guideline1, guideline2, guideline3, guideline4, home, items, loading, pause, question, result, shop
from UI.assets import media_path
from UI.clue_outcome import ClueOutcomeResolver
from UI.stats_persistence import RunStatsPersistence

pygame.init()
pygame.font.init()
pygame.mixer.init()


class Game:
    """Main pygame loop"""

    # UI_states
    QUIT, HOME, PAUSE, GUIDE1, GUIDE2, GUIDE3, GUIDE4, CHAR, BOARD, LOADING, QUESTION, RESULT, SHOP, BAG, GET_READY, GAME_OVER, ROUND_SUMMARY, DAILY_DOUBLE, FINAL_WAGER = range(19)

    def __init__(self):
        """Create display, initialize scores and AI players, construct every UI window used in ``run``."""
        self.running = True
        self.state = self.HOME
        self.prev_state = self.HOME
        self.round_no = 1
        self.selected_pos = (-1, -1)  # (row, col)
        self.question_list = None
        self.data_ready = False
        self.generating = False
        self.generation_failed = False

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Jeopardy")
        self.clock = pygame.time.Clock()
        self.ui_dir = Path(__file__).resolve().parent

        self.player_name = "Player"
        self.player_char = media_path("Game Assets", "Characters", "c1.png") or (
            self.ui_dir / "Game Assets" / "Characters" / "c1.png"
        )
        self.player_score = 0
        self.ai_score1 = 0
        self.ai_score2 = 0
        self.human_correct_clues = 0  # count the number of correct answers (use to compare when the score is drawn equally)
        self.ai_players = [AIPlayer("AI_1"), AIPlayer("AI_2")]
        self.question_start_ms = 0
        self.question_time_limit_sec: int | None = None
        self.daily_double_targets = {1: set(), 2: set()}  # round_no: (row, col)
        self.daily_double_used = {1: set(), 2: set()}     # consumed positions per round
        self.current_question_is_daily_double = False
        self.current_question_wager = 0
        self.final_eligible_ai = [True, True]
        self.final_eligible_human = True
        self.ai_final_wagers = [0, 0]
        self.human_final_wager = 0
        self.final_ai_done = [True, True]
        self.final_ai_correct: list[bool | None] = [None, None]
        self.final_human_done = True
        self.final_human_correct: bool | None = None
        self._fj_ai_score_before_answer: list[int | None] = [None, None]
        self._fj_human_score_before_answer: int | None = None
        self.menu_return_state = self.BOARD
        self.pause_just_opened = False
        self._bgm_paused_for_overlay = False
        self.active_human_item = 0
        self.human_double_active = False
        self.human_shield_active = False

        self.loading_window = loading.loading(self.screen)
        self.home_window = home.Homepage(self.screen)
        self.pause_window = pause.pause_window(self.screen)
        self.character_window = char.Character(self.screen)
        self.question_board = board.question_board(self.screen, self.round_no)
        self.question_window = question.Question(self.screen)
        self.guidelines_window = guideline1.Guidelines(self.screen, self.ui_dir.parent / "Guideline.txt")
        self.guidelines_window2 = guideline2.Guidelines(self.screen, self.ui_dir.parent / "Guideline.txt")
        self.guidelines_window3 = guideline3.Guidelines(self.screen, self.ui_dir.parent / "Guideline.txt")
        self.guidelines_window4 = guideline4.Guidelines(self.screen, self.ui_dir.parent / "Guideline.txt")
        self.result_window = result.Result(self.screen)
        self.shop_window = shop.Shop(self.screen)
        self.items_window = items.Shop(self.screen)
        self.daily_double_window = daily_double.dailydouble(self.screen)
        self.get_ready_window = get_ready.GetReady(self.screen, self.round_no)
        self.game_over_window = game_over.GameOver(self.screen)
        self._stats = RunStatsPersistence(ROOT_DIR)
        self._clues = ClueOutcomeResolver(self)

    def _configure_wager_window(self, final_round: bool):
        """Reuse daily_double UI for both Daily Double and Final Jeopardy wager."""
        if final_round:
            self.daily_double_window.title = "FINAL JEOPARDY"
            self.daily_double_window.wager_text = "YOUR FINAL JEOPARDY WAGER:"
            self.daily_double_window.wager_min = 0
        else:
            self.daily_double_window.title = "YOU FOUND A DAILY DOUBLE!"
            self.daily_double_window.wager_text = "YOUR WAGER:"
            self.daily_double_window.wager_min = 5
        self.daily_double_window.current_warning = ""
        self.daily_double_window.text = ""
        self.daily_double_window.active = False

    def _prepare_ai_for_current_question(self):
        """Use AI logic to answer."""
        row, col = self.selected_pos
        q = self.question_list[f"round{self.round_no}"][col]["questions"][row]
        options = q.get("options", [])
        correct = int(q.get("correct", 0))
        if len(options) <= 0:
            return
        now = pygame.time.get_ticks()
        for idx, ai in enumerate(self.ai_players):
            if self.round_no == 3 and not self.final_eligible_ai[idx]:
                ai.cancel_pending()
                continue
            ai.prepare_choice(
                correct_option_index=correct,
                num_options=len(options),
                current_time_ms=now,
                round_no=self.round_no,
            )

    def _sync_ai_scores(self):
        """sync AI scores to the board"""
        self.ai_score1 = self.ai_players[0].score
        self.ai_score2 = self.ai_players[1].score
        self.question_board.update_score(self.player_score, self.ai_score1, self.ai_score2)

    def _get_current_question_payload(self):
        return self._clues.get_payload()

    def _resolve_question_by_winner(self, winner: str, is_correct: bool):
        """Apply score and stats for the first responder, clear wager."""
        self._clues.resolve_first_responder(winner, is_correct)

    def _clear_clue_wager_and_boost_flags(self) -> None:
        self.current_question_is_daily_double = False
        self.current_question_wager = 0
        self.active_human_item = 0
        self.human_double_active = False
        self.human_shield_active = False

    def _apply_equipped_item_for_question(self):
        if self.round_no == 3:
            # Final Jeopardy: same rule as Daily Double
            if self.items_window.has_equipped_item():
                self.items_window.invalidate_equipped_item_no_consume()
            self.active_human_item = 0
            self.question_window.set_hidden_options(set())
            self.human_double_active = False
            self.human_shield_active = False
            return False
        self.active_human_item = self.items_window.get_equipped_item_no()
        self.question_window.set_hidden_options(set())
        self.human_double_active = False
        self.human_shield_active = False
        if self.active_human_item == 1:
            self.items_window.consume_equipped_item()
            self.result_window.update_custom_message("Skip used! No score change.", "")
            self.active_human_item = 0
            return True
        if self.active_human_item == 2:
            q = self._get_current_question_payload()
            correct_idx = int(q.get("correct", 0))
            num_options = len(q.get("options", []))
            wrong_indices = [i for i in range(num_options) if i != correct_idx]
            random.shuffle(wrong_indices)
            self.question_window.set_hidden_options(set(wrong_indices[:1]))
            self.items_window.consume_equipped_item()
            self.active_human_item = 0
            return False
        if self.active_human_item == 3:
            self.human_double_active = True
            self.items_window.consume_equipped_item()
            self.active_human_item = 0
            return False
        if self.active_human_item == 4:
            self.human_shield_active = True
            self.items_window.consume_equipped_item()
            self.active_human_item = 0
            return False
        return False

    def _setup_final_jeopardy_turn_state(self) -> None:
        """score must be > 0 to answer,else wager 0 and locked"""
        self.final_eligible_ai = [self.ai_players[i].score > 0 for i in range(2)]
        self.final_eligible_human = self.player_score > 0
        self.ai_final_wagers = []
        for i in range(2):
            if self.final_eligible_ai[i]:
                mx = max(0, int(self.ai_players[i].score))
                self.ai_final_wagers.append(random.randint(0, mx))
            else:
                self.ai_final_wagers.append(0)
        self.human_final_wager = int(self.current_question_wager) if self.final_eligible_human else 0
        self.final_ai_done = [not self.final_eligible_ai[i] for i in range(2)]
        self.final_ai_correct = [None, None]
        self.final_human_done = not self.final_eligible_human
        self.final_human_correct = None
        self._fj_ai_score_before_answer = [None, None]
        self._fj_human_score_before_answer = None

    def _fj_all_answered(self) -> bool:
        if not self.final_human_done:
            return False
        for i in range(2):
            if self.final_eligible_ai[i] and not self.final_ai_done[i]:
                return False
        return True

    def _apply_final_ai_outcome(self, idx: int, is_correct: bool) -> None:
        self._fj_ai_score_before_answer[idx] = int(self.ai_players[idx].score)
        w = int(self.ai_final_wagers[idx])
        if is_correct:
            self.ai_players[idx].correct_clues += 1
            self.ai_players[idx].add_score(w)
        else:
            self.ai_players[idx].subtract_score(w)
        self.final_ai_correct[idx] = is_correct
        self._sync_ai_scores()

    def _apply_final_human_outcome(self, is_correct: bool) -> None:
        self._fj_human_score_before_answer = int(self.player_score)
        w = int(self.human_final_wager)
        self.final_human_correct = is_correct
        if is_correct:
            self.human_correct_clues += 1
            self.player_score += w
            self.result_window.correct_sound.play()
        else:
            self.player_score -= w
            self.result_window.wrong_sound.play()

    def fj_status_rows(self) -> list[dict]:
        rows: list[dict] = []
        for idx in range(2):
            name = self.ai_players[idx].name
            w = int(self.ai_final_wagers[idx])
            sc = int(self.ai_players[idx].score)
            if not self.final_eligible_ai[idx]:
                rows.append(
                    {"kind": "player", "name": name, "can_play": False, "wager": 0, "score": sc, "phase": "spectator"}
                )
                continue
            if not self.final_ai_done[idx]:
                rows.append(
                    {"kind": "player", "name": name, "can_play": True, "wager": w, "score": sc, "phase": "answering"}
                )
            else:
                before = self._fj_ai_score_before_answer[idx]
                if before is None:
                    before = sc
                rows.append(
                    {
                        "kind": "player",
                        "name": name,
                        "can_play": True,
                        "wager": w,
                        "score": int(before),
                        "phase": "answered",
                    }
                )
        rows.append({"kind": "sep"})
        if not self.final_eligible_human:
            rows.append(
                {
                    "kind": "player",
                    "name": self.player_name,
                    "can_play": False,
                    "wager": 0,
                    "score": int(self.player_score),
                    "phase": "spectator",
                }
            )
        elif not self.final_human_done:
            rows.append(
                {
                    "kind": "player",
                    "name": self.player_name,
                    "can_play": True,
                    "wager": int(self.human_final_wager),
                    "score": int(self.player_score),
                    "phase": "answering",
                }
            )
        else:
            before = self._fj_human_score_before_answer
            if before is None:
                before = int(self.player_score)
            rows.append(
                {
                    "kind": "player",
                    "name": self.player_name,
                    "can_play": True,
                    "wager": int(self.human_final_wager),
                    "score": int(before),
                    "phase": "answered",
                }
            )
        return rows

    def _finish_final_jeopardy_to_result(self) -> None:
        for ai in self.ai_players:
            ai.cancel_pending()
        self.question_window.reset_final_jeopardy_mode()
        self.current_question_is_daily_double = False
        self.current_question_wager = 0
        q = self._get_current_question_payload()
        options = q.get("options", [])
        correct_idx = int(q.get("correct", 0))
        correct_answer_text = ""
        if isinstance(options, list) and 0 <= correct_idx < len(options):
            correct_answer_text = str(options[correct_idx])
        self.result_window.set_final_jeopardy_result(
            "Final Jeopardy",
            self.build_fj_result_rows(),
            correct_answer_text,
        )
        self.state = self.RESULT

    def build_fj_result_rows(self) -> list[tuple[str, str]]:
        rows: list[tuple[str, str]] = []
        if not self.final_eligible_human:
            rows.append((f"{self.player_name} did not play.", "+$0"))
        else:
            ok = self.final_human_correct
            w = int(self.human_final_wager)
            if ok:
                rows.append((f"{self.player_name} answered correctly!", f"+${w}"))
            else:
                rows.append((f"{self.player_name} answered incorrectly!", f"-${w}"))
        for idx in range(2):
            n = self.ai_players[idx].name
            if not self.final_eligible_ai[idx]:
                rows.append((f"{n} did not play.", "+$0"))
            else:
                ok = self.final_ai_correct[idx]
                w = int(self.ai_final_wagers[idx])
                if ok:
                    rows.append((f"{n} answered correctly!", f"+${w}"))
                else:
                    rows.append((f"{n} answered incorrectly!", f"-${w}"))
        return rows

    def enter_question_state(self):
        """Start question timer, apply items."""
        self.question_start_ms = pygame.time.get_ticks()
        if self.round_no in (1, 2):
            self.question_time_limit_sec = 7
        else:
            self.question_time_limit_sec = None
        self.question_window.set_countdown(self.question_time_limit_sec)
        skip_used = self._apply_equipped_item_for_question()
        if skip_used:
            for ai in self.ai_players:
                ai.cancel_pending()
            self._clear_clue_wager_and_boost_flags()
            self.state = self.RESULT
            return
        if self.round_no == 3:
            self._setup_final_jeopardy_turn_state()
            self._prepare_ai_for_current_question()
            self.question_window.configure_final_jeopardy(self.final_eligible_human)
        else:
            self.question_window.reset_final_jeopardy_mode()
            self._prepare_ai_for_current_question()
        self.state = self.QUESTION

    def start_generation_if_needed(self):
        """start background thread to generate questions if not already ready/running"""
        if self.generating or self.data_ready:
            return
        self.generation_failed = False
        self.generating = True
        threading.Thread(target=self.generate_questions, daemon=True).start()

    @staticmethod
    def _enforce_round_values(data: dict):
        """Normalize clue values"""
        r1_vals = [200, 400, 600, 800, 1000]
        r2_vals = [v * 2 for v in r1_vals]
        for rkey, vals in (("round1", r1_vals), ("round2", r2_vals)):
            rounds = data.get(rkey, [])
            if not isinstance(rounds, list):
                continue
            for cat in rounds:
                if not isinstance(cat, dict):
                    continue
                qs = cat.get("questions", [])
                if not isinstance(qs, list):
                    continue
                for i, q in enumerate(qs[:5]):
                    if isinstance(q, dict):
                        q["value"] = vals[i]

    def _parse_llm_questions(self, raw: str) -> dict:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in LLM output.")
        data = json.loads(raw[start:end])
        if not is_valid_question_pack(data):
            raise ValueError("LLM question pack is missing categories or options.")
        return data

    def generate_questions(self):
        try:
            data = None
            if not LLM.use_offline_questions() and LLM.has_api_key():
                try:
                    data = self._parse_llm_questions(LLM.q_generate(LLM.prompt))
                except Exception:
                    data = None
            if data is None:
                data = load_offline_questions()
            if not is_valid_question_pack(data):
                raise ValueError("Question pack is invalid.")
            self.question_list = data
            self._enforce_round_values(self.question_list)
            all_cells = [(r, c) for r in range(5) for c in range(6)]
            self.daily_double_targets = {
                1: set(random.sample(all_cells, 1)),
                2: set(random.sample(all_cells, 2)),
            }
            self.daily_double_used = {1: set(), 2: set()}
            self.data_ready = True
            self.generation_failed = False
        except Exception:
            self.question_list = None
            self.data_ready = False
            self.generation_failed = True
        finally:
            self.generating = False

    def game_over_ranking_rows(self) -> list[list]:
        """Rows for GameOver: [avatar, name, score, correct_clues]"""
        return [
            [self.player_char, self.player_name, self.player_score, self.human_correct_clues],
            ["AI_1", "AI_1", self.ai_score1, self.ai_players[0].correct_clues],
            ["AI_2", "AI_2", self.ai_score2, self.ai_players[1].correct_clues],
        ]

    def reset_scores_and_answer_stats(self):
        self.player_score = 0
        self.ai_score1 = 0
        self.ai_score2 = 0
        self.human_correct_clues = 0
        for ai in self.ai_players:
            ai.score = 0
            ai.correct_clues = 0

    def load_stats_from_disk(self) -> None:
        """Load username"""
        self._stats.load_into_shop_and_bag(self.player_name, self.shop_window, self.items_window)

    def finalize_run_stats_and_save(self) -> tuple[int, int]:
        return self._stats.finalize_run(
            self.player_name,
            self.player_score,
            self.human_correct_clues,
            self.ai_score1,
            self.ai_score2,
            self.ai_players,
            self.shop_window,
            self.items_window,
        )

    def restart_run_keep_character(self):
        """New game from current name"""
        self.selected_pos = (-1, -1)
        self.reset_scores_and_answer_stats()
        self.question_list = None
        self.data_ready = False
        self.generating = False
        self.generation_failed = False
        self.daily_double_targets = {1: set(), 2: set()}
        self.daily_double_used = {1: set(), 2: set()}
        self.final_eligible_ai = [True, True]
        self.final_eligible_human = True
        self.current_question_is_daily_double = False
        self.current_question_wager = 0
        self.active_human_item = 0
        self.human_double_active = False
        self.human_shield_active = False
        self.menu_return_state = self.BOARD
        self.question_window.reset_final_jeopardy_mode()

    def _set_round(self, round_no: int):
        """switch round"""
        self.round_no = round_no
        if self.round_no in (1, 2):
            self.question_board = board.question_board(self.screen, self.round_no)
            self.question_board.update_questions(self.question_list, self.round_no)
            self.question_board.update_character(self.player_name, self.player_char)
            self.question_board.update_score(self.player_score, self.ai_score1, self.ai_score2)
        self.get_ready_window = get_ready.GetReady(self.screen, self.round_no)
        self.get_ready_window.sync_round_no(
            self.round_no,
            [
                self.question_board,
                self.question_window,
                self.shop_window,
                self.items_window,
                self.result_window,
            ],
        )

    def _prep_final_jeopardy_after_round_gate(self) -> None:
        """Enter Final Jeopardy wager"""
        self.final_eligible_ai = [self.ai_score1 > 0, self.ai_score2 > 0]
        self.final_eligible_human = self.player_score > 0
        if self.items_window.has_equipped_item():
            self.items_window.invalidate_equipped_item_no_consume()
        self.selected_pos = (0, 0)
        self.question_window.update_question(self.round_no, self.question_list, self.selected_pos)
        self._configure_wager_window(final_round=True)
        self.daily_double_window.update_character(self.player_char)
        self.daily_double_window.text = ""
        self.daily_double_window.current_warning = ""
        if self.final_eligible_human:
            self.state = self.FINAL_WAGER
        else:
            self.current_question_is_daily_double = True
            self.current_question_wager = 0
            self.enter_question_state()

    def _is_round_finished(self) -> bool:
        """True when every question has been selected."""
        pressed = [v for k, v in vars(self.question_board).items() if k.endswith("_pressed")]
        return bool(pressed) and all(pressed)

    def draw_prev_for_pause(self):
        """frozen backdrop"""
        if self.prev_state == self.HOME:
            self.home_window.draw()
        elif self.prev_state in (self.CHAR,):
            self.character_window.draw()
        elif self.prev_state in (self.BOARD,):
            self.question_board.draw()
        elif self.prev_state in (self.LOADING,):
            self.loading_window.draw()
        elif self.prev_state in (self.SHOP,):
            self.shop_window.draw()
        elif self.prev_state in (self.BAG,):
            self.items_window.draw()
        elif self.prev_state in (self.QUESTION,):
            self.question_window.draw()
        elif self.prev_state in (self.GET_READY,):
            self.get_ready_window.draw()
        elif self.prev_state in (self.GAME_OVER,):
            self.game_over_window.draw()

    def run(self):
        """main loop"""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state == self.QUIT:
                self.running = False

            elif self.state == self.HOME:
                n = self.home_window.update(events)
                self.home_window.draw()
                if n == 3:
                    self.state = self.CHAR
                elif n == 4:
                    self.state = self.GUIDE1
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.HOME

            elif self.state == self.CHAR:
                action = self.character_window.update(events)
                self.character_window.draw()
                if action == "START":
                    self.reset_scores_and_answer_stats()
                    self.player_name = self.character_window.text.strip() or "Player"
                    self.player_char = self.character_window.avatar_paths[self.character_window.selected_idx]
                    self.state = self.LOADING
                    self.start_generation_if_needed()
                elif action == "QUIT":
                    self.state = self.PAUSE
                self.prev_state = self.CHAR

            elif self.state == self.LOADING:
                ret = self.loading_window.update(events, self.data_ready, self.generation_failed)
                if ret == 6:
                    self.start_generation_if_needed()
                elif ret == 1 and self.data_ready:
                    self.load_stats_from_disk()
                    self._set_round(1)
                    self.state = self.GET_READY
                self.loading_window.draw(self.generation_failed)
                self.prev_state = self.LOADING

            elif self.state == self.GET_READY:
                n = self.get_ready_window.update(events)
                self.get_ready_window.draw()
                if n == 4:
                    if self.round_no == 3:
                        self._prep_final_jeopardy_after_round_gate()
                    else:
                        self.state = self.BOARD
                elif n == 10:
                    self.menu_return_state = self.GET_READY
                    self.state = self.SHOP
                elif n == 11:
                    self.menu_return_state = self.GET_READY
                    self.state = self.BAG
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.GET_READY

            elif self.state == self.BOARD:
                n, row, col = self.question_board.update(events)
                self.question_board.draw()
                if n == 8 and row >= 0 and col >= 0:
                    self.selected_pos = (row, col)
                    if (
                        self.round_no in (1, 2)
                        and (row, col) in self.daily_double_targets.get(self.round_no, set())
                        and (row, col) not in self.daily_double_used.get(self.round_no, set())
                    ):
                        # Daily Double disables any pre-equipped item without consuming inventory.
                        if self.items_window.has_equipped_item():
                            self.items_window.invalidate_equipped_item_no_consume()
                        self._configure_wager_window(final_round=False)
                        self.daily_double_window.update_character(self.player_char)
                        self.state = self.DAILY_DOUBLE
                    else:
                        self.current_question_is_daily_double = False
                        self.current_question_wager = 0
                        self.question_window.update_question(self.round_no, self.question_list, self.selected_pos)
                        self.enter_question_state()
                elif n == 10:
                    self.menu_return_state = self.BOARD
                    self.state = self.SHOP
                elif n == 11:
                    self.menu_return_state = self.BOARD
                    self.state = self.BAG
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.BOARD

            elif self.state == self.DAILY_DOUBLE:
                self.question_board.draw()
                n, wager = self.daily_double_window.update(events, self.player_score)
                self.daily_double_window.draw()
                if n == 2:
                    if self.round_no in (1, 2):
                        self.daily_double_used.setdefault(self.round_no, set()).add(self.selected_pos)
                    self.current_question_is_daily_double = True
                    self.current_question_wager = int(wager)
                    self.question_window.update_question(self.round_no, self.question_list, self.selected_pos)
                    self.enter_question_state()
                self.prev_state = self.DAILY_DOUBLE

            elif self.state == self.FINAL_WAGER:
                n, wager = self.daily_double_window.update(events, self.player_score)
                self.daily_double_window.draw()
                if n == 2:
                    # Final wager applies to human score only
                    self.current_question_is_daily_double = True
                    self.current_question_wager = int(wager)
                    self.question_window.update_question(self.round_no, self.question_list, self.selected_pos)
                    self.enter_question_state()
                self.prev_state = self.FINAL_WAGER

            elif self.state == self.QUESTION:
                now = pygame.time.get_ticks()
                elapsed_sec = (now - self.question_start_ms) / 1000.0

                if self.round_no == 3:
                    self.question_window.set_countdown(None)
                    q_pre = self._get_current_question_payload()
                    cidx_pre = int(q_pre.get("correct", 0))
                    for idx, ai in enumerate(self.ai_players):
                        if not self.final_eligible_ai[idx] or self.final_ai_done[idx]:
                            continue
                        ai_idx = ai.check_time_and_answer(now)
                        if ai_idx is not None:
                            self._apply_final_ai_outcome(idx, ai_idx == cidx_pre)
                            self.final_ai_done[idx] = True
                elif self.question_time_limit_sec is None:
                    self.question_window.set_countdown(None)
                else:
                    remaining = max(0, int(self.question_time_limit_sec - elapsed_sec))
                    self.question_window.set_countdown(remaining)

                n, ok = self.question_window.update(events)

                if self.round_no == 3:
                    if n == 9 and self.final_eligible_human and not self.final_human_done:
                        self._apply_final_human_outcome(bool(ok))
                        self.final_human_done = True
                    if n == 7 and self._fj_all_answered():
                        self._finish_final_jeopardy_to_result()
                    self.question_window.set_final_jeopardy_overlay(
                        self.fj_status_rows(),
                        self._fj_all_answered(),
                        self.final_human_done,
                    )
                    self.question_window.draw()
                else:
                    self.question_window.draw()

                    human_candidate = None
                    if n == 9:
                        human_candidate = (now, "human", bool(ok))

                    q = self._get_current_question_payload()
                    correct_idx = int(q.get("correct", 0))
                    ai_candidates = []
                    for idx, ai in enumerate(self.ai_players):
                        ai_idx = ai.check_time_and_answer(now)
                        if ai_idx is not None:
                            ai_correct = ai_idx == correct_idx
                            who = "ai_1" if idx == 0 else "ai_2"
                            ai_candidates.append((ai.target_time_ms, who, ai_correct))

                    candidates = []
                    if human_candidate is not None:
                        candidates.append(human_candidate)
                    candidates.extend(ai_candidates)
                    if candidates:
                        candidates.sort(key=lambda x: x[0])
                        _, who, is_correct = candidates[0]
                        self._resolve_question_by_winner(who, is_correct)
                        self.state = self.RESULT
                    elif self.question_time_limit_sec is not None and elapsed_sec >= self.question_time_limit_sec:
                        for ai in self.ai_players:
                            ai.cancel_pending()
                        self._clear_clue_wager_and_boost_flags()
                        self.result_window.update_custom_message("Time is up! No one answered.", "", "")
                        self.state = self.RESULT
                self.prev_state = self.QUESTION

            elif self.state == self.RESULT:
                n = self.result_window.update(events)
                self.result_window.draw()
                if n == 2:
                    if self.round_no == 3:
                        # Final round (no short summary).
                        human_score_snapshot = int(self.player_score)
                        self.game_over_window.update_result(self.game_over_ranking_rows())
                        best_score, win_streak = self.finalize_run_stats_and_save()
                        self.game_over_window.set_personal_records(best_score, win_streak)
                        self.game_over_window.set_coins_added_display(human_score_snapshot)
                        self.reset_scores_and_answer_stats()
                        self.state = self.GAME_OVER
                    elif self._is_round_finished():
                        self.get_ready_window.set_round_summary(
                            self.round_no,
                            self.player_name,
                            self.player_score,
                            self.ai_score1,
                            self.ai_score2,
                        )
                        # Short round summary
                        self.game_over_window.winning_sound.play()
                        self.state = self.ROUND_SUMMARY
                    else:
                        self.state = self.BOARD
                self.prev_state = self.RESULT

            elif self.state == self.ROUND_SUMMARY:
                n = self.get_ready_window.update(events)
                self.get_ready_window.draw()
                if n == 4:
                    advanced = self.get_ready_window.try_advance_round(
                        self.question_board,
                        [
                            self.question_board,
                            self.question_window,
                            self.shop_window,
                            self.items_window,
                            self.result_window,
                        ],
                    )
                    next_round = self.get_ready_window.round_no if advanced else self.round_no + 1
                    self._set_round(next_round)
                    self.state = self.GET_READY
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.ROUND_SUMMARY

            elif self.state == self.SHOP:
                n = self.shop_window.update(events)
                purchased_item_no = self.shop_window.pop_purchased_item()
                if purchased_item_no:
                    self.items_window.update_contents(purchased_item_no)
                self.shop_window.draw()
                if n == 6:
                    self.state = self.menu_return_state
                elif n == 11:
                    self.state = self.BAG
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.SHOP

            elif self.state == self.BAG:
                n = self.items_window.update(events)
                self.items_window.draw()
                if n == 6:
                    self.state = self.menu_return_state
                elif n == 10:
                    self.state = self.SHOP
                elif n == 2:
                    self.state = self.PAUSE
                self.prev_state = self.BAG

            elif self.state == self.GUIDE1:
                n = self.guidelines_window.update(events)
                self.guidelines_window.draw()
                if n == 2:
                    self.state = self.GUIDE2
                elif n == 5:
                    self.state = self.HOME
                self.prev_state = self.GUIDE1

            elif self.state == self.GUIDE2:
                n = self.guidelines_window2.update(events)
                self.guidelines_window2.draw()
                if n == 1:
                    self.state = self.GUIDE1
                elif n == 3:
                    self.state = self.GUIDE3
                elif n == 5:
                    self.state = self.HOME
                self.prev_state = self.GUIDE2

            elif self.state == self.GUIDE3:
                n = self.guidelines_window3.update(events)
                self.guidelines_window3.draw()
                if n == 2:
                    self.state = self.GUIDE2
                elif n == 4:
                    self.state = self.GUIDE4
                elif n == 5:
                    self.state = self.HOME
                self.prev_state = self.GUIDE3

            elif self.state == self.GUIDE4:
                n = self.guidelines_window4.update(events)
                self.guidelines_window4.draw()
                if n == 3:
                    self.state = self.GUIDE3
                elif n == 5:
                    self.state = self.HOME
                self.prev_state = self.GUIDE4

            elif self.state == self.GAME_OVER:
                n = self.game_over_window.update(events)
                self.game_over_window.draw()
                if n == 3:
                    self.restart_run_keep_character()
                    self.state = self.LOADING
                    self.start_generation_if_needed()
                elif n == 4:
                    self.prev_state = self.GAME_OVER
                    self.state = self.PAUSE
                    self.pause_just_opened = True
                elif n == 2:
                    self.state = self.HOME
                    self.reset_scores_and_answer_stats()
                    self.data_ready = False
                    self.generation_failed = False
                    self.question_list = None
                    self.daily_double_targets = {1: set(), 2: set()}
                    self.daily_double_used = {1: set(), 2: set()}
                    self.final_eligible_ai = [True, True]
                    self.final_eligible_human = True
                    self.question_window.reset_final_jeopardy_mode()
                    self.start_generation_if_needed()
                self.prev_state = self.GAME_OVER

            elif self.state == self.PAUSE:
                self.draw_prev_for_pause()
                if self.pause_just_opened:
                    n = self.PAUSE
                    self.pause_just_opened = False
                else:
                    n = self.pause_window.update(events, self.prev_state)
                self.pause_window.draw()
                if n == 0:
                    self.state = self.QUIT
                elif n != self.PAUSE:
                    self.state = n

            want_pause_bgm = self.state in (
                self.PAUSE,
                self.GET_READY,
                self.ROUND_SUMMARY,
                self.GAME_OVER,
            )
            if want_pause_bgm and not self._bgm_paused_for_overlay:
                pygame.mixer.music.pause()
                self._bgm_paused_for_overlay = True
            elif not want_pause_bgm and self._bgm_paused_for_overlay:
                pygame.mixer.music.unpause()
                self._bgm_paused_for_overlay = False

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    Game().run()