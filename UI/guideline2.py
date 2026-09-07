"""Tutorial page 2 — thin wrapper so ``guideline2.Guidelines`` stays stable for Client."""

try:
    from .guidelines_pages import GuidelinesPage2 as Guidelines
except ImportError:
    import sys
    from pathlib import Path

    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from UI.guidelines_pages import GuidelinesPage2 as Guidelines

__all__ = ["Guidelines"]
