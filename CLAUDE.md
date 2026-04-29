# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Ignition_NQFinder is a Python utility that searches Ignition Perspective project JSON configuration files for Named Query (NQ) references. It outputs results to a CSV file for analysis.

## Running the Script

```bash
python src/lookForNQPaths.py
```

No dependencies beyond the Python standard library (`csv`, `json`, `os`). No build step, no virtual environment needed.

## Architecture

All logic lives in a single file: `src/lookForNQPaths.py`.

**Key functions:**
- `find_locations_by_string(data, target, path, parent_name)` — recursively traverses a JSON structure, tracking the key path and nearest parent name whenever the target string is found.
- `find_view_json_files(root_dir)` — walks a directory tree and yields paths to all `view.json` files.
- `main()` — iterates over hardcoded target Named Query names, searches all discovered `view.json` files, and writes findings to `results.csv`.

**Hardcoded values to be aware of:**
- The root search path is a Windows filesystem path: `C:\Program Files\Inductive Automation\Ignition\...` — update this when running on a different machine or project.
- The four target NQ names (`umGetCBPChartData`, `uspGetTasklistGroupEntity`, `uspGetSFZoneGroupName`, `uspAdhocHourAdd`) are defined directly in `main()`.

**Output:** `results.csv` written to the working directory, with columns for the view file path, key path within the JSON, parent element name, and matched target string.
