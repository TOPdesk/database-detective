"""mkdocs-macros-plugin hook module.

Lets the workshop content branch between two database targets from a single
set of markdown files, instead of maintaining them as separate git branches.
Selected via the WORKSHOP_VARIANT environment variable at build/serve time:

    WORKSHOP_VARIANT=mssql uv run mkdocs build    # default
    WORKSHOP_VARIANT=duckdb uv run mkdocs build

Inside a markdown file, branch on the `variant` variable this exposes, e.g.:

    {% if variant == "duckdb" %}
    ...DuckDB-specific text/SQL...
    {% else %}
    ...MSSQL-specific text/SQL...
    {% endif %}
"""
import os

VARIANTS = ("mssql", "duckdb")


def define_env(env):
    variant = os.environ.get("WORKSHOP_VARIANT", "mssql")
    if variant not in VARIANTS:
        raise ValueError(f"WORKSHOP_VARIANT={variant!r} is not one of {VARIANTS}")
    env.variables["variant"] = variant
