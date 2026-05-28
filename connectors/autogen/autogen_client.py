"""AutoGen integration helper for AIAgentOrchestration.

This module provides a minimal, safe scaffold for integrating the AutoGen
agent orchestration runtime. It intentionally avoids calling into unknown
AutoGen internals so it is safe to import even when `autogen` is not
installed. Use the functions here as a starting point for adding a
real orchestration runner.

See connectors/autogen/README.md for usage and installation notes.
"""
from typing import Optional


def is_available() -> bool:
    """Return True if the `autogen` package can be imported."""
    try:
        import autogen  # type: ignore

        return True
    except Exception:
        return False


def get_version() -> Optional[str]:
    """Return the detected `autogen` package version, or None if missing."""
    try:
        import autogen  # type: ignore

        return getattr(autogen, "__version__", None)
    except Exception:
        return None


def generate_example_snippet() -> str:
    """Return a small example code snippet that demonstrates how to start
    a simple AutoGen orchestration. This is a template for users to copy
    into their own code once `autogen` is installed.
    """
    return """
# Example AutoGen orchestration (template) — paste into a script after
# installing `autogen` (pip install autogen)
from autogen import Autogen  # adjust imports to the installed version

def run_simple_orchestration(api_key: str):
    # This is a minimal template. Refer to AutoGen docs for full examples.
    ag = Autogen(api_key=api_key)
    # create agents, tools, and run interactions according to your design
    # e.g. ag.create_agent(...), ag.run(...)

if __name__ == "__main__":
    import os
    run_simple_orchestration(os.getenv("OPENAI_API_KEY"))
"""


def demo_info() -> str:
    """Return a short human-friendly string describing integration state."""
    if is_available():
        ver = get_version() or "unknown"
        return f"AutoGen is installed (version={ver}). See connectors/autogen/README.md for next steps."
    return "AutoGen is not installed. Run `pip install autogen` to enable the connector."
