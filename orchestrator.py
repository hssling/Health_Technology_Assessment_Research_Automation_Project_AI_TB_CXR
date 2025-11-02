#!/usr/bin/env python3
"""
HTA Orchestrator
Run from the PARENT folder that contains:
    hta_project_01_hpv_vaccine/
    hta_project_02_ncd_screening/
    ...
This script will:
1. Detect all hta_project_* dirs
2. For each project:
    - read protocol
    - read search strings
    - run R dedupe script (if R available)
    - run Python model
    - assemble final_report.md
Outputs go to: <project>/output/
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from literature_search import perform_literature_search
from data_processor import process_project_data
from manuscript_generator import generate_manuscript

# ---------------- CONFIG ----------------
PARENT_DIR = Path(".").resolve()
PROJECT_PREFIX = "hta_project_"
RUN_ALL_PROJECTS = True   # set to False to run only the first detected
PYTHON_MODEL_PREFIX = "04_"
R_SCRIPT_NAME = "05_lit_processing.R"
PROTOCOL_PREFIX = "01_protocol_"
SEARCH_PREFIX = "02_search_strings.txt"
EXTRACTION_FILE = "03_data_extraction_template.csv"
MANUSCRIPT_FILE = "06_manuscript_template.md"
# ----------------------------------------


def find_projects(parent: Path):
    projects = []
    for item in parent.iterdir():
        if item.is_dir() and item.name.startswith(PROJECT_PREFIX):
            projects.append(item)
    return sorted(projects)


def read_text_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def run_r_script(project_dir: Path, log_lines: list):
    r_path = project_dir / R_SCRIPT_NAME
    if not r_path.exists():
        log_lines.append(f"R: {R_SCRIPT_NAME} not found, skipping.")
        return

    # Ensure output dir
    (project_dir / "output").mkdir(exist_ok=True)

    try:
        # This assumes `Rscript` is in PATH
        cmd = ["Rscript", str(r_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        log_lines.append("R: executed.")
        if result.stdout:
            log_lines.append("R stdout:\n" + result.stdout)
        if result.stderr:
            log_lines.append("R stderr:\n" + result.stderr)
    except FileNotFoundError:
        log_lines.append("R: Rscript not found on system PATH. Skipping.")


def run_python_model(project_dir: Path, log_lines: list):
    # find file starting with 04_
    model_files = [p for p in project_dir.iterdir() if p.is_file() and p.name.startswith(PYTHON_MODEL_PREFIX) and p.suffix == ".py"]
    if not model_files:
        log_lines.append("Model: no 04_* python model found, skipping.")
        return None

    model_file = model_files[0]
    try:
        cmd = ["python", str(model_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_dir)
        log_lines.append(f"Model: executed {model_file.name}")
        if result.stdout:
            log_lines.append("Model stdout:\n" + result.stdout)
        if result.stderr:
            log_lines.append("Model stderr:\n" + result.stderr)
        # try to parse key lines from stdout
        return result.stdout
    except FileNotFoundError:
        log_lines.append("Model: python not found.")
        return None


def assemble_final_report(project_dir: Path,
                          protocol_text: str,
                          search_text: str,
                          model_stdout: str,
                          log_lines: list):
    out_dir = project_dir / "output"
    out_dir.mkdir(exist_ok=True)

    # Try to read manuscript template
    manuscript_path = project_dir / MANUSCRIPT_FILE
    manuscript_text = read_text_if_exists(manuscript_path)

    # Build JSON results (very simple)
    results_json = {
        "project": project_dir.name,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "model_stdout": model_stdout,
        "log": log_lines,
    }
    (out_dir / "results.json").write_text(json.dumps(results_json, indent=2), encoding="utf-8")

    # Build final_report.md
    report_lines = []
    report_lines.append(f"# HTA Automation Report – {project_dir.name}")
    report_lines.append("")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("## 1. Protocol (parsed)")
    report_lines.append(protocol_text if protocol_text else "_Protocol file not found._")
    report_lines.append("")
    report_lines.append("## 2. Search Strategy")
    report_lines.append(search_text if search_text else "_Search strings file not found._")
    report_lines.append("")
    report_lines.append("## 3. Model Output (stdout)")
    report_lines.append("```")
    report_lines.append(model_stdout if model_stdout else "Model did not produce output or was not run.")
    report_lines.append("```")
    report_lines.append("")
    report_lines.append("## 4. Draft Manuscript (template)")
    report_lines.append(manuscript_text if manuscript_text else "_Manuscript template not found._")
    report_lines.append("")
    report_lines.append("## 5. Orchestrator Log")
    report_lines.append("```")
    report_lines.extend(log_lines)
    report_lines.append("```")

    (out_dir / "final_report.md").write_text("\n".join(report_lines), encoding="utf-8")


def process_project(project_dir: Path):
    log_lines = [f"=== Processing project: {project_dir.name} ==="]

    # 1. read protocol
    protocol_files = [p for p in project_dir.iterdir() if p.name.startswith(PROTOCOL_PREFIX) and p.suffix == ".md"]
    protocol_text = read_text_if_exists(protocol_files[0]) if protocol_files else ""
    if protocol_text:
        log_lines.append("Protocol: loaded.")
    else:
        log_lines.append("Protocol: NOT found.")

    # 2. read search
    search_text = read_text_if_exists(project_dir / SEARCH_PREFIX)
    if search_text:
        log_lines.append("Search strings: loaded.")
    else:
        log_lines.append("Search strings: NOT found.")

    # 3. perform literature search
    log_lines.append("Literature search: starting...")
    extracted_data = perform_literature_search(project_dir)
    if extracted_data:
        log_lines.append(f"Literature search: completed, extracted {len(extracted_data)} data points.")
    else:
        log_lines.append("Literature search: failed or no data extracted.")

    # 4. process extracted data
    log_lines.append("Data processing: starting...")
    df_filled = process_project_data(project_dir)
    if df_filled is not None:
        log_lines.append(f"Data processing: completed, filled {len(df_filled)} rows.")
    else:
        log_lines.append("Data processing: failed or no data to process.")

    # 5. run R
    run_r_script(project_dir, log_lines)

    # 4. run model
    model_stdout = run_python_model(project_dir, log_lines)

    # 5. generate manuscript
    log_lines.append("Manuscript generation: starting...")
    manuscript = generate_manuscript(project_dir)
    log_lines.append("Manuscript generation: completed.")

    # 6. assemble report
    assemble_final_report(project_dir, protocol_text, search_text, model_stdout, log_lines)

    print(f"[OK] HTA automation complete for {project_dir.name}")


def main():
    projects = find_projects(PARENT_DIR)
    if not projects:
        print("No hta_project_* folders found in this directory.")
        return

    if RUN_ALL_PROJECTS:
        for proj in projects:
            process_project(proj)
    else:
        process_project(projects[0])


if __name__ == "__main__":
    main()
