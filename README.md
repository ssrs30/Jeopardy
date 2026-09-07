# Jeopardy

A CUHK AIST1110 group project: a Jeopardy-style quiz game built with Python and pygame.  
One human player competes against two AI opponents, with a shop, Daily Double, Final Jeopardy, and local save data.

**You can play without an API key.** The game will use the bundled question pack.

## Requirements

- Python 3.10 or later
- Packages listed in `requirements.txt` (`pygame`, `openai`, `python-dotenv`)

```bash
python -m pip install -r requirements.txt
python main.py
```

Controls: click buttons and board tiles with the mouse. Close the window or confirm Quit in the pause menu to exit.  
Full rules are available from the homepage **HELP** button, or in `Guideline.txt`.

## API key (optional)

This repository does **not** include a real key. Fill one in only if you want the LLM to generate a new question set.

1. Copy the template:

```bash
copy API.env.example API.env
```

On macOS / Linux:

```bash
cp API.env.example API.env
```

2. Edit `API.env` and add **your** key:

```env
AZURE_API_KEY=your_key_here
AZURE_BASE_URL=https://cuhk-apip.azure-api.net/openai-eus2/openai/v1
AZURE_MODEL=gpt-4o
USE_OFFLINE_QUESTIONS=0
```

- CUHK students: request a key from the [CUHK API Portal](https://cuhk-apip.developer.azure-api.net/)
- Other users: set `AZURE_BASE_URL` and `AZURE_MODEL` to an OpenAI-compatible endpoint you control
- To always use the bundled questions: set `USE_OFFLINE_QUESTIONS=1`

Do not commit `API.env`. Do not paste a live key into issues or chat.  
If the key is empty or the request fails, the game loads `offline_questions.py` automatically.

## Optional pixel font

`Pix32.ttf` is **not** included, because the font license forbids redistribution.  
To restore the original pixel look, download the font yourself and place `Pix32.ttf` in the project root or the `UI/` folder.  
If the file is missing, the game falls back to the default pygame font.

Font source: [Pix32 on dafont](https://www.dafont.com/pix32.font)

## Project layout

```
main.py                 entry point
LLM.py                  optional LLM question generator
offline_questions.py    bundled question pack (used when no key is set)
contestants.py          AI opponents
Guideline.txt           in-game help text
API.env.example         key template (copy to API.env)
UI/                     screens and main loop
Game Assets/            images
Sound Effect/           audio
```

## License

Original source code is released under the MIT License. See `LICENSE`.  
Third-party art, audio, and fonts remain under their own terms. See `ATTRIBUTION.md`.
