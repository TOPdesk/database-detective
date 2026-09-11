The workshop materials are built using mkdocs, a python markdown-based static site generator.
Dependencies are managed with [uv](https://docs.astral.sh/uv/) and declared in `pyproject.toml`.

## Development

If you want develop & preview your changes locally, you can run

```sh
uv sync
# (this creates a .venv with mkdocs installed into it)
uv run mkdocs serve
```

Now point your browser to http://localhost:8000

It's also possible to generate all static files locally to check the directory structure.

```sh
uv run mkdocs build
# static files will be placed in the ./public directory
```