"""Per-user ``stats.json`` persistence (coin, items, scores, streak) — used by ``Game`` without UI logic."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RunStatsPersistence:

    USER_DEFAULTS: dict = {
        "coin": 2000,
        "items": {"1": 0, "2": 0, "3": 0, "4": 0},
        "last_score": 0,
        "best_score": 0,
        "win_streak": 0,
        "games_played": 0,
    }

    def __init__(self, root_dir: Path) -> None:
        self._root_dir = root_dir

    def stats_json_path(self) -> Path:
        return self._root_dir / "stats.json"

    @staticmethod
    def username_key(player_name: str) -> str:
        return (player_name or "Player").strip() or "Player"

    def merge_user_stats_record(self, raw: object) -> dict:
        rec = {k: (dict(v) if k == "items" else v) for k, v in self.USER_DEFAULTS.items()}
        if not isinstance(raw, dict):
            return rec
        if isinstance(raw.get("coin"), (int, float)):
            rec["coin"] = max(0, int(raw["coin"]))
        it = raw.get("items")
        if isinstance(it, dict):
            for key in ("1", "2", "3", "4"):
                v = it.get(key)
                if isinstance(v, (int, float)):
                    rec["items"][key] = max(0, int(v))
        for key in ("last_score", "best_score", "win_streak", "games_played"):
            v = raw.get(key)
            if isinstance(v, (int, float)):
                rec[key] = int(v)
        return rec

    def merge_flat_legacy_into_user_record(self, flat: dict) -> dict:
        rec = self.merge_user_stats_record(None)
        if isinstance(flat.get("coin"), (int, float)):
            rec["coin"] = max(0, int(flat["coin"]))
        it = flat.get("items")
        if isinstance(it, dict):
            rec["items"] = self.merge_user_stats_record({"items": it})["items"]
        for key in ("last_score", "best_score", "win_streak", "games_played"):
            v = flat.get(key)
            if isinstance(v, (int, float)):
                rec[key] = int(v)
        return rec

    def load_full_stats_root(self) -> dict:
        """load stats.json"""
        path = self.stats_json_path()
        if not path.is_file():
            return {"users": {}}
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"users": {}}
        if not isinstance(data, dict):
            return {"users": {}}
        users = data.get("users")
        if isinstance(users, dict) and users:
            out = {k: v for k, v in data.items()}
            out["users"] = {str(k): self.merge_user_stats_record(v) for k, v in users.items()}
            return out
        if isinstance(users, dict) and not users:
            return {k: v for k, v in data.items() if k != "users"} | {"users": {}}
        legacy_rec = self.merge_flat_legacy_into_user_record(data)
        return {"users": {"Player": legacy_rec}}

    def write_stats_root(self, root: dict) -> None:
        """Write json"""
        path = self.stats_json_path()
        users = root.get("users")
        if not isinstance(users, dict):
            root = {"users": {}}
        else:
            root = {k: v for k, v in root.items()}
            root["users"] = dict(users)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(root, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def load_into_shop_and_bag(self, player_name: str, shop_window: Any, items_window: Any) -> None:
        root = self.load_full_stats_root()
        users = root.setdefault("users", {})
        if not isinstance(users, dict):
            return
        uname = self.username_key(player_name)
        created = False
        if uname not in users:
            users[uname] = self.merge_user_stats_record(None)
            created = True
        cur = self.merge_user_stats_record(users.get(uname))
        shop_window.coin = int(cur["coin"])
        for key, attr in (
            ("1", "icon1_no"),
            ("2", "icon2_no"),
            ("3", "icon3_no"),
            ("4", "icon4_no"),
        ):
            setattr(items_window, attr, int(cur["items"].get(key, 0)))
        if items_window.has_equipped_item():
            items_window.invalidate_equipped_item_no_consume()
        items_window.skip_consume_on_return = False
        if created:
            self.write_stats_root(root)

    @staticmethod
    def human_finished_first(
        player_name: str,
        player_score: int,
        human_correct_clues: int,
        ai_score1: int,
        ai_score2: int,
        ai_players: list,
    ) -> bool:
        human = (
            str(player_name) if player_name else "Player",
            int(player_score),
            int(human_correct_clues),
        )
        ranked = [
            human,
            ("AI_1", int(ai_score1), int(ai_players[0].correct_clues)),
            ("AI_2", int(ai_score2), int(ai_players[1].correct_clues)),
        ]
        ranked.sort(key=lambda x: (x[1], x[2]), reverse=True)
        top = ranked[0]
        return top[0] == human[0] and top[1] == human[1] and top[2] == human[2]

    def finalize_run(
        self,
        player_name: str,
        player_score: int,
        human_correct_clues: int,
        ai_score1: int,
        ai_score2: int,
        ai_players: list,
        shop_window: Any,
        items_window: Any,
    ) -> tuple[int, int]:
        """Coin += max(0, score)/persist user row"""
        end_score = int(player_score)
        shop_window.coin += max(0, end_score)
        root = self.load_full_stats_root()
        users = root.setdefault("users", {})
        if not isinstance(users, dict):
            users = {}
            root["users"] = users
        uname = self.username_key(player_name)
        if uname not in users:
            users[uname] = self.merge_user_stats_record(None)
        cur = self.merge_user_stats_record(users.get(uname))
        cur["coin"] = int(shop_window.coin)
        cur["items"] = {
            "1": int(items_window.icon1_no),
            "2": int(items_window.icon2_no),
            "3": int(items_window.icon3_no),
            "4": int(items_window.icon4_no),
        }
        cur["last_score"] = end_score
        cur["best_score"] = max(int(cur["best_score"]), end_score)
        if self.human_finished_first(
            player_name, player_score, human_correct_clues, ai_score1, ai_score2, ai_players
        ):
            cur["win_streak"] = int(cur["win_streak"]) + 1
        else:
            cur["win_streak"] = 0
        cur["games_played"] = int(cur["games_played"]) + 1
        users[uname] = cur
        self.write_stats_root(root)
        return int(cur["best_score"]), int(cur["win_streak"])
