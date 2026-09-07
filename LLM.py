"""Optional LLM question generator. The game runs without a key via offline questions."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o"


def _load_env_files() -> None:
    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / "API.env")
    load_dotenv(base_dir / ".env")


def settings() -> dict[str, str]:
    _load_env_files()
    return {
        "api_key": (os.getenv("AZURE_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip(),
        "base_url": (
            os.getenv("AZURE_BASE_URL") or os.getenv("OPENAI_BASE_URL") or DEFAULT_BASE_URL
        ).strip(),
        "model": (os.getenv("AZURE_MODEL") or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL).strip(),
    }


def has_api_key() -> bool:
    return bool(settings()["api_key"])


def use_offline_questions() -> bool:
    _load_env_files()
    flag = (os.getenv("USE_OFFLINE_QUESTIONS") or "").strip().lower()
    return flag in {"1", "true", "yes", "on"}


def get_client() -> OpenAI:
    cfg = settings()
    if not cfg["api_key"]:
        raise RuntimeError(
            "AZURE_API_KEY is empty. Copy API.env.example to API.env and fill in your key, "
            "or set USE_OFFLINE_QUESTIONS=1 to play the bundled question set."
        )
    return OpenAI(
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
        default_headers={"api-key": cfg["api_key"]},
        timeout=30.0,
    )


def q_generate(user_prompt: str) -> str:
    cfg = settings()
    response = get_client().chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM returned an empty response.")
    return content


prompt = """\
Please generate trivia content for a Jeopardy-style game in THREE rounds.

Rounds 1 and 2 (full boards):
Exactly 6 categories, in this order: "Science", "History", "Literature", "Geography", "Film", "Math".
Each category has exactly 5 questions.
Each question has 3 short answer options (do not prefix with "what is") and "correct" as the 0-based index.
Round 1 question values per category must be exactly 200, 400, 600, 800, 1000 (easiest at 200).
Round 2 question values must be EXACTLY DOUBLE of Round 1 values at the same row position: 400, 800, 1200, 1600, 2000.
Overall difficulty: round1 ≈ 2/10, round2 ≈ 6/10.

Round 3 (Final Jeopardy — NOT a full board):
Generate EXACTLY ONE category and EXACTLY ONE question inside it.
Pick one category name at random from the six above.
Use a single high-stakes "value" for that one question (e.g. 2000). Difficulty ≈ 10/10.
Same 3-option format as other rounds.

Output: one JSON object only (no markdown, no commentary). Keys: "round1", "round2", "round3".
- round1 and round2: array of exactly 6 objects, each { "name": "<category>", "questions": [ ... 5 question objects ... ] }.
- round3: array of ONE object only: { "name": "<chosen category>", "questions": [ ONE question object ] }.

Each question object shape:
{ "value": <int>, "question": "<clue text>", "options": ["...", "...", "..."], "correct": <0|1|2> }
"""


if __name__ == "__main__":
    if not has_api_key():
        print("No API key set. Copy API.env.example to API.env and add AZURE_API_KEY.")
    else:
        print(q_generate(prompt))
