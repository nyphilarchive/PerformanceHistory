# Performance History Pipeline (Automation)

This repo contains a single-command pipeline to refresh the NY Phil Performance History dataset from Solr and regenerate the canonical XML and JSON files.

## Prerequisites

- Java runtime on PATH (to run Saxon XSLT)
- Python 3.9+ and `pip`
- Node.js (to run the XML→JSON converter)

## One‑command refresh

Windows PowerShell:

```
./tools/sync.ps1  # optionally: -Solr http://your-solr/solr/assets/select
```

macOS/Linux:

```
./tools/sync.sh  # prefers Python 3.8; auto-creates .venv if needed; uses SOLR_URL or ./.env
```

Set the Solr endpoint via `SOLR_URL` (in `.env` or your environment) or pass `-Solr` to the PowerShell script. There is no built‑in default.

Notes:
- The POSIX sync script prefers Python 3.8 when available. If an existing `.venv` uses <3.8 and `python3.8` is present, it will recreate `.venv` with 3.8.
- It auto‑creates `.venv` and installs minimal Python deps (from `requirements.txt`) if missing. The PowerShell variant does not auto‑create by default; use a venv if needed.

### Environment configuration

- `.env.example` is provided as a template. Copy to `.env` and set `SOLR_URL` for local runs without passing flags.
- `.env` is git‑ignored and intended for non‑secret config like internal service URLs. Do not store credentials in the repo.

## What the pipeline does

1. Downloads XML from Solr into `pre-transform/`:
   - `complete.xml` (full set)
   - Date‑range segments mirroring existing filenames
2. Runs the XSLT in `pre-transform/cleanxmls.xsl` via Saxon to produce normalized XML in `Programs/xml/`
3. Rewrites those XML files with `Scripts/reformat_xml.py`
4. Converts XML→JSON via `Scripts/XmlToJson/app.js` into `Programs/json/`

All paths are resolved relative to the repo root. The Saxon JAR bundled in `tools/saxon/` is used (with fallback to `saxon/` for backward compatibility).

## Manual use of substeps

```
python tools/pipeline.py download --solr http://your-solr/solr/assets/select
python tools/pipeline.py transform
python tools/pipeline.py reformat
python tools/pipeline.py json
```

## Scheduling options

- Windows: create a Task Scheduler job that runs `powershell -File sync.ps1`
- Linux/macOS: add a cron entry (e.g., weekly) to run `bash /path/to/repo/sync.sh`
- GitHub Actions: use a self‑hosted runner on the internal network to run `./sync.sh` on a `schedule:` trigger

> Note: The Solr endpoint in use is on a private network; Actions will require a self‑hosted runner with network access.
