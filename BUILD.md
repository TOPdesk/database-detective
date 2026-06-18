The workshop materials are built using mkdocs, a python markdown-based static site generator.

## Development

If you want develop & preview your changes locally, you can run

```sh
pip3 install -r requirements.txt 
# (this should install the mkdocs command in your path)
mkdocs serve
```

Now point your browser to http://localhost:8000

It's also possible to generate all static files locally to check the directory structure.

```sh
mkdocs build
# static files will be placed in the ./public directory
```