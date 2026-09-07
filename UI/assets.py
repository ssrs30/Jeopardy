"""Resolve images, sounds, and fonts from either project-root or UI copies."""
from __future__ import annotations

from pathlib import Path

import pygame

ROOT_DIR = Path(__file__).resolve().parent.parent
UI_DIR = Path(__file__).resolve().parent


class NullSound:
    def play(self, *args, **kwargs):
        return None

    def set_volume(self, *args, **kwargs):
        return None

    def stop(self, *args, **kwargs):
        return None


def _norm(name: str) -> str:
    return name.lower().replace(" ", "").replace("_", "").replace("-", "")


def media_path(*parts: str) -> Path | None:
    """Find a media file under Game Assets / Sound Effect in root or UI."""
    if not parts:
        return None
    relative = Path(*parts)
    exact_candidates = [
        ROOT_DIR / relative,
        UI_DIR / relative,
    ]
    for path in exact_candidates:
        if path.is_file():
            return path

    folder = relative.parent
    filename = relative.name
    for base in (ROOT_DIR, UI_DIR):
        directory = base / folder
        if not directory.is_dir():
            continue
        wanted = _norm(filename)
        for item in directory.iterdir():
            if item.is_file() and _norm(item.name) == wanted:
                return item
    return None


def load_image(*parts: str, size: tuple[int, int] = (240, 80), label: str = "") -> pygame.Surface:
    path = media_path(*parts)
    if path is not None:
        try:
            return pygame.image.load(str(path)).convert_alpha()
        except Exception:
            pass
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((70, 70, 70, 255))
    pygame.draw.rect(surf, (210, 210, 210), surf.get_rect(), 2)
    font = pygame.font.Font(None, max(18, min(size) // 3))
    txt = font.render((label or Path(*parts).stem)[:16], True, (255, 255, 255))
    surf.blit(txt, txt.get_rect(center=surf.get_rect().center))
    return surf


def load_sound(*parts: str):
    path = media_path(*parts)
    if path is None:
        return NullSound()
    try:
        return pygame.mixer.Sound(str(path))
    except Exception:
        return NullSound()


def play_music(*parts: str, volume: float = 0.3, loops: int = -1) -> bool:
    path = media_path(*parts)
    if path is None:
        return False
    try:
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play(loops)
        return True
    except Exception:
        return False


def load_font(size: int):
    for candidate in (ROOT_DIR / "Pix32.ttf", UI_DIR / "Pix32.ttf"):
        if candidate.is_file():
            try:
                return pygame.freetype.Font(str(candidate), size)
            except Exception:
                continue
    return pygame.freetype.Font(None, size)
