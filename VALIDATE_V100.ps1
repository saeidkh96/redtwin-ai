$ErrorActionPreference = 'Stop'
python -m pytest -q
python -m ruff check .
python -m redtwin.demo
