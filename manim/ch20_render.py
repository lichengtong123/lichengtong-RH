"""Shared display settings; numerical formulas do not depend on the theme."""
import os

from manim import Text, config


BOOK_MODE = os.environ.get("RH_RENDER_MODE", "video").lower() == "book"
PREVIEW = os.environ.get("RH_PREVIEW", "0") == "1"
ENGLISH = os.environ.get("RH_LANGUAGE", "zh").lower() == "en"


def localized(chinese, english):
    return english if ENGLISH else chinese


def caption_text(text, font_size=48, **kwargs):
    if not ENGLISH:
        return Text(text, font_size=font_size, **kwargs)
    # Shape at a larger size to avoid small-font glyph-position quantization.
    return Text(text, font_size=font_size * 4, **kwargs).scale(0.25)


def configure_render():
    width, height = (2880, 1620) if BOOK_MODE else (1920, 1080)
    if PREVIEW:
        width, height = 960, 540
    config.pixel_width = width
    config.pixel_height = height
    config.frame_rate = 30
    config.background_color = "#FFFFFF"
    if ENGLISH:
        config.media_dir = "media/en"
        # Explicit Latin typography avoids platform-dependent fallback spacing.
        Text.set_default(font="Arial", disable_ligatures=True)
    if BOOK_MODE:
        config.save_last_frame = True
        config.write_to_movie = False


THEME = {
    "foreground": "#171717",
    "muted": "#666666",
    "grid": "#B8B8B8",
    "main": "#171717",
    "boundary": "#287A48",
    "zero": "#B32332",
    "blue": "#185A9D",
    "orange": "#A64D12",
    "cyan": "#006B83",
}
