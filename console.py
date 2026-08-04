# =============================================================
#  MYTHOS-SYNC FRAMEWORK — CONSOLE SETUP
#  Shared by every entry point. Import and call before printing.
# =============================================================

import sys


def use_utf8_output():
    """Force UTF-8 on stdout/stderr so the engine's output survives Windows.

    Every module prints box-drawing characters and emoji. Windows consoles
    default to cp1252, which cannot encode them, so an unguarded run dies with
    UnicodeEncodeError before printing a single line. This never surfaced on
    Replit, where stdout is UTF-8 already.

    Safe to call more than once, and safe when stdout has been replaced by
    something that isn't a real stream — a StringIO under redirect_stdout has
    no reconfigure(), which is exactly the case the tests exercise.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            # Detached or otherwise not reconfigurable. Printing falls back to
            # the platform default, which is where we started.
            pass
