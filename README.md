# StringFinder Process Scanner

A Python tool for scanning running processes for specific strings using `xxstrings64.exe`. Results are saved to `results.txt` file.

## Features
- Scans all running processes for user-defined strings
- Uses `xxstrings64.exe` for string extraction from process memory
- Results include process name, PID, and process creation date
- Results are always overwritten

## Requirements
- Python 3.7+
- `psutil` package
- `xxstrings64.exe` (must be in the same directory or in PATH)

## Setup
1. Install Python dependencies:
   ```bash
   pip install psutil
   ```
2. Place `xxstrings64.exe` in the same folder as this script or ensure it is in your system PATH.
3. Create a `strings.txt` file in the same folder. Each line should be a string to search for in process memory.

## Usage
Run the scanner from the command line:
```bash
python scanner.py
```

## How It Works
- Loads search strings from `strings.txt`
- Iterates over all running processes
- For each process, runs `xxstrings64.exe -p <PID>` to extract strings
- Checks for matches with the search strings
- Writes results to `results.txt` (overwriting previous results)

## Output
- `results.txt` contains:
  - Process Name
  - PID
  - Creation Date
- Only processes with matches are listed
- Example output:
  ```
  Process Name | PID | Creation Date
  ============================================================
  notepad.exe | 1234 | 2025-09-13 10:15:00
  chrome.exe | 5678 | 2025-09-13 09:45:22
  ```

## Notes
- If no matches are found, `results.txt` will only contain the header.
- If `strings.txt` is missing or empty, the tool will exit with an error message.
