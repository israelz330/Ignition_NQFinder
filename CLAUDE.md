# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a single-script Python utility that scans Ignition Perspective `view.json` files for Named Query (NQ) references (stored procedure names or named query identifiers) and writes all matches to a `results.csv` file.

## Running the Script

```bash
python src/lookForNQPaths.py
```

No dependencies beyond the Python standard library (`csv`, `json`, `os`).

## Key Customization Points

Before running, edit `src/lookForNQPaths.py` directly:

1. **Target strings** — the list of Named Query names to search for:
   ```python
   target_strings = ['uspGetTasklistGroupEntity', ...]
   ```

2. **Folder path** — the root directory containing Ignition Perspective `view.json` files, passed to `find_view_json_files(...)` inside `main()`. Currently hardcoded to a Windows path:
   ```
   C:\Program Files\Inductive Automation\Ignition\data\projects\global\com.inductiveautomation.perspective\views
   ```

## Architecture

The script has three functions that compose a linear pipeline:

- **`find_view_json_files(folder_path)`** — walks the directory tree and collects all files named exactly `view.json`.
- **`find_locations_by_string(data, target_string, path, parent_names)`** — recursively traverses a parsed JSON structure (dicts and lists). Tracks the current key path as a list and collects `meta/name` values into a `parent_names` stack to reconstruct human-readable component names. Returns a list of `{targetString, parentName, keyPath}` dicts for every node whose string value contains the target.
- **`main()`** — iterates every `(target_string, view.json file)` pair, calls the two functions above, and writes rows to `results.csv`. The `parentName` column is assembled from the last five path segments of the file path (split on `\`).

## Platform Notes

The script has two Windows-specific assumptions:
- The default `folder_path` uses a Windows absolute path with backslashes.
- `os.startfile('results.csv')` at the end opens the CSV with the default application (Windows only); remove or replace this line when running on Linux/macOS.
- The `parent_name` assembly in `main()` uses `file_path.split('\\')`, which only works correctly on Windows path strings.
