#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

try:
    import requests
except Exception:
    requests = None


REPO_ROOT = Path(__file__).resolve().parents[1]
PRETRANSFORM_DIR = REPO_ROOT / "pre-transform"
PROGRAMS_XML_DIR = REPO_ROOT / "Programs" / "xml"
PROGRAMS_JSON_DIR = REPO_ROOT / "Programs" / "json"
def resolve_saxon() -> Path:
    candidates = [
        REPO_ROOT / "tools" / "saxon" / "saxon9he.jar",
        REPO_ROOT / "saxon" / "saxon9he.jar",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

SAXON_JAR = resolve_saxon()
XSLT_PATH = PRETRANSFORM_DIR / "cleanxmls.xsl"
PY_REFORMAT = REPO_ROOT / "Scripts" / "reformat_xml.py"
XML_TO_JSON_DIR = REPO_ROOT / "Scripts" / "XmlToJson"


DEFAULT_SOLR = os.environ.get(
    "SOLR_URL",
    "http://192.168.198.156:9993/solr/assets/select",
)


FIELDS = (
    "id,"
    "*ProgramID,*SubEventName,*LocationName,*VenueName,*Time,"
    "*OrchestraName,*Season,*Date,*ComposerWorksTitle_facet,"
    "*WorksComposerNames,*WorksShortTitle,*Encore,*WorksSoloistNames,"
    "*WorksSoloistInstrumentNames,*WorksSoloistFunction,*WorksConductorNames,"
    "*ProgramWorksIDs,*WorksMovIDs,*WorksTitle,*timestamp"
)


SEGMENTS: List[Dict[str, str]] = [
    {
        "label": "1842-43_TO_1910-11",
        "season_range": "[1842-43 TO 1910-11]",
        "pre_name": "1-1000.xml",
    },
    {
        "label": "1911-12_TO_1919-20",
        "season_range": "[1911-12 TO 1919-20]",
        "pre_name": "1001-2000.xml",
    },
    {
        "label": "1920-21_TO_1925-26",
        "season_range": "[1920-21 TO 1925-26]",
        "pre_name": "2001-3000.xml",
    },
    {
        "label": "1926-27_TO_1931-32",
        "season_range": "[1926-27 TO 1931-32]",
        "pre_name": "3001-4000.xml",
    },
    {
        "label": "1932-33_TO_1939-40",
        "season_range": "[1932-33 TO 1939-40]",
        "pre_name": "4001-5000.xml",
    },
    {
        "label": "1940-41_TO_1946-47",
        "season_range": "[1940-41 TO 1946-47]",
        "pre_name": "5001-6000.xml",
    },
    {
        "label": "1947-48_TO_1954-55",
        "season_range": "[1947-48 TO 1954-55]",
        "pre_name": "6001-7000.xml",
    },
    {
        "label": "1955-56_TO_1962-63",
        "season_range": "[1955-56 TO 1962-63]",
        "pre_name": "7001-8000.xml",
    },
    {
        "label": "1963-64_TO_1973-74",
        "season_range": "[1963-64 TO 1973-74]",
        "pre_name": "8001-9000.xml",
    },
    {
        "label": "1974-75_TO_1983-84",
        "season_range": "[1974-75 TO 1983-84]",
        "pre_name": "9001-10000.xml",
    },
    {
        "label": "1984-85_TO_1994-95",
        "season_range": "[1984-85 TO 1994-95]",
        "pre_name": "10001-11000.xml",
    },
    {
        "label": "1995-96_TO_2003-04",
        "season_range": "[1995-96 TO 2003-04]",
        "pre_name": "11001-12000.xml",
    },
    {
        "label": "2004-05_TO_2010-11",
        "season_range": "[2004-05 TO 2010-11]",
        "pre_name": "12001-13000.xml",
    },
    {
        "label": "2011-12_TO_2023-24",
        "season_range": "[2011-12 TO 2023-24]",
        "pre_name": "13001-15000.xml",
    },
    {
        "label": "2024-25_TO_NOW",
        "season_range": "[2024-25 TO NOW]",
        "pre_name": "15001-16000.xml",
    },
]


def ensure_dirs():
    PRETRANSFORM_DIR.mkdir(parents=True, exist_ok=True)
    PROGRAMS_XML_DIR.mkdir(parents=True, exist_ok=True)
    PROGRAMS_JSON_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd: List[str], cwd: Optional[Path] = None):
    print(f"$ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def download_segment(solr_url: str, label: str, season_range: str, pre_name: str, rows: int = 2000):
    if not requests:
        print("Python 'requests' is not installed. Install dependencies first: pip install -r requirements.txt")
        raise SystemExit(1)
    params = {
        "q": 'nyp\\:DocumentType:"Program"',
        "rows": rows,
        "omitHeader": "true",
        "sort": "npp:SortDate asc",
        "fl": FIELDS,
        "wt": "xml",
        "indent": "true",
        # use filter query for the season range
        "fq": f"npp\\:Season:{season_range}",
    }
    print(f"Downloading segment {label} → {pre_name}")
    resp = requests.post(solr_url, data=params, timeout=120)
    resp.raise_for_status()
    out_path = PRETRANSFORM_DIR / pre_name
    out_path.write_bytes(resp.content)


def download_all(solr_url: str):
    # complete.xml (full set)
    if not requests:
        print("Python 'requests' is not installed. Install dependencies first: pip install -r requirements.txt")
        raise SystemExit(1)
    print("Downloading complete.xml (full dataset)...")
    params = {
        "q": 'nyp\\:DocumentType:"Program"',
        "rows": 15000,
        "omitHeader": "true",
        "sort": "npp:SortDate asc",
        "fl": FIELDS,
        "wt": "xml",
        "indent": "true",
    }
    resp = requests.post(solr_url, data=params, timeout=300)
    resp.raise_for_status()
    (PRETRANSFORM_DIR / "complete.xml").write_bytes(resp.content)

    for seg in SEGMENTS:
        download_segment(solr_url, seg["label"], seg["season_range"], seg["pre_name"])


def require_java():
    try:
        subprocess.run(["java", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        print("Java runtime not found on PATH. Install Java (JRE/JDK) to run Saxon transforms.")
        raise SystemExit(1)
    if not SAXON_JAR.exists():
        print(f"Saxon JAR not found at {SAXON_JAR}. Ensure the repository's 'saxon' folder is present.")
        raise SystemExit(1)


def transform_one(source_xml: Path, output_xml: Path):
    require_java()
    if not XSLT_PATH.exists():
        print(f"XSLT not found at {XSLT_PATH}")
        raise SystemExit(1)
    cmd = [
        "java",
        "-Xmx1g",
        "-jar",
        str(SAXON_JAR),
        f"-s:{source_xml}",
        f"-o:{output_xml}",
        f"-xsl:{XSLT_PATH}",
    ]
    run(cmd)


def transform_all():
    # transform complete.xml
    src = PRETRANSFORM_DIR / "complete.xml"
    dst = PROGRAMS_XML_DIR / "complete.xml"
    if src.exists():
        print("Transforming complete.xml...")
        transform_one(src, dst)
    else:
        print("Warning: pre-transform/complete.xml not found; skipping full transform.")

    # transform each segment
    for seg in SEGMENTS:
        src = PRETRANSFORM_DIR / seg["pre_name"]
        dst = PROGRAMS_XML_DIR / f"{seg['label']}.xml"
        if src.exists():
            print(f"Transforming {seg['pre_name']} → {dst.name}")
            transform_one(src, dst)
        else:
            print(f"Warning: {src} not found; skipping.")


def reformat_xml():
    if not PY_REFORMAT.exists():
        print(f"Reformat script not found at {PY_REFORMAT}")
        raise SystemExit(1)
    # Execute in repo root so script's chdir works as expected
    run([sys.executable, str(PY_REFORMAT)], cwd=REPO_ROOT)


def xml_to_json():
    # Ensure node is available
    try:
        subprocess.run(["node", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        print("Node.js is required to run the XML→JSON step. Install Node and npm.")
        raise SystemExit(1)
    # Dependencies likely already vendored; attempt to run app.js
    run(["node", "app.js"], cwd=XML_TO_JSON_DIR)


def main():
    parser = argparse.ArgumentParser(description="NY Phil Performance History automation pipeline")
    sub = parser.add_subparsers(dest="cmd")

    p_all = sub.add_parser("all", help="Run full pipeline: download → transform → reformat → json")
    p_all.add_argument("--solr", default=DEFAULT_SOLR, help="Solr select URL")

    p_dl = sub.add_parser("download", help="Download XML from Solr into pre-transform")
    p_dl.add_argument("--solr", default=DEFAULT_SOLR, help="Solr select URL")

    sub.add_parser("transform", help="Run XSLT to produce Programs/xml/* from pre-transform")
    sub.add_parser("reformat", help="Reformat Programs/xml/* for consistency")
    sub.add_parser("json", help="Convert Programs/xml/* to Programs/json/*")

    args = parser.parse_args()
    if getattr(args, "cmd", None) is None:
        parser.print_help()
        sys.exit(2)
    ensure_dirs()

    if args.cmd == "download":
        download_all(args.solr)
    elif args.cmd == "transform":
        transform_all()
    elif args.cmd == "reformat":
        reformat_xml()
    elif args.cmd == "json":
        xml_to_json()
    elif args.cmd == "all":
        download_all(args.solr)
        transform_all()
        reformat_xml()
        xml_to_json()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
