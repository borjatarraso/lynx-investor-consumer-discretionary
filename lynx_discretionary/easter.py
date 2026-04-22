"""Easter-egg shim over :mod:`lynx_investor_core.easter`.

Binds consumer-discretionary labels and fortune quotes so call sites stay
unchanged.  Also re-exports the legacy constants (LYNX_ASCII, WOLF_ASCII,
BULL_ASCII, PICKAXE_ASCII, FORTUNE_QUOTES, ROCKET_ASCII) for callers that
reference them directly (e.g. the Textual TUI).
"""

from __future__ import annotations

from lynx_investor_core import easter as _core_easter
from lynx_investor_core.easter import (  # noqa: F401
    BULL_ASCII,
    GENERIC_FORTUNES,
    ROCKET_ASCII,
    WOLF_ASCII,
)

_CONSUMER_FORTUNES = (
    '"The customer is always right — in matters of taste." \u2014 Harry Gordon Selfridge',
    '"Your most unhappy customers are your greatest source of learning." \u2014 Bill Gates',
    '"Retail is detail." \u2014 James Gulliver',
    '"In retail, you live and die by the comp." \u2014 Retail proverb',
    '"A brand is the sum of the good, the bad, the ugly, and the off-strategy." \u2014 Scott Bedbury',
)

FORTUNE_QUOTES = tuple(GENERIC_FORTUNES) + _CONSUMER_FORTUNES

_EGG = _core_easter.AgentEasterEgg(
    label="Consumer Discretionary Analysis",
    sublabel="Consumer Discretionary Research",
    banner_prog="lynx-discretionary",
    extra_fortunes=_CONSUMER_FORTUNES,
)

# Pre-rendered ASCII variants (legacy callers that import these directly).
LYNX_ASCII = _core_easter._lynx_ascii(_EGG.label)
PICKAXE_ASCII = _core_easter._pickaxe_ascii(_EGG.sublabel)


def rich_matrix(console, duration: float = 3.0) -> None:
    _core_easter.rich_matrix(console, duration=duration)


def rich_fortune(console) -> None:
    _core_easter.rich_fortune(console, _EGG)


def rich_rocket(console) -> None:
    _core_easter.rich_rocket(console)


def rich_lynx(console) -> None:
    _core_easter.rich_lynx(console, _EGG)


def tk_fireworks(root) -> None:
    _core_easter.tk_fireworks(root, _EGG)


def tk_rainbow_title(root, count: int = 20) -> None:
    _core_easter.tk_rainbow_title(root, _EGG, count=count)
