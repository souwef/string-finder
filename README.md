# StringFinder Process Scanner

A powerful command-line tool for scanning running processes to detect specific strings using memory analysis. This tool uses `xxstrings64.exe` to extract strings from process memory and matches them against user-defined patterns.

## Features

- **Process Memory Scanning**: Scan all running processes for specific string patterns
- **Custom String Database**: Load search patterns from `strings.txt`
- **Memory Analysis**: Uses `xxstrings64.exe` for advanced string extraction from process memory
- **Results Logging**: Saves findings to `results.txt` with comprehensive details
- **Portable**: Can be compiled into a standalone executable

## ⚠️ Administrator Privileges Required

**This tool REQUIRES administrator privileges to function properly** because it:
- Uses `xxstrings64.exe` to scan process memory
- Accesses running process memory spaces

**Always run as Administrator:**
- **Python script**: Right-click Command Prompt → "Run as administrator", then run `python scanner.py`
- **Executable**: Right-click `scanner.exe` → "Run as administrator"

## Requirements

### For Running from Source
- Python 3.7 or higher
- Required Python packages:
  - `psutil`
- `xxstrings64.exe` (included)
- `strings.txt` file with search patterns

### For Standalone Executable
- No requirements - the executable is self-contained
- Administrator privileges required for memory scanning

## Installation & Usage

### Option 1: Running from Source

1. **Install Python dependencies**:
   ```powershell
   pip install psutil
   ```

2. **Create search patterns file**:
   - Create `strings.txt` in the same folder
   - Add one search string per line

3. **Run as Administrator**:
   ```powershell
   # Open Command Prompt as Administrator, then:
   python scanner.py
   ```

### Option 2: Use Standalone Executable

1. **Download or build** `scanner.exe` from the `dist` folder
2. **Create `strings.txt`** in the same directory as the executable
3. **Right-click `scanner.exe` → "Run as administrator"**

## How to Use

1. **Prepare search strings**:
   - Create or edit `strings.txt`
   - Add one search pattern per line
   - Example:
     ```
     malicious_string
     suspicious_pattern
     cheat_signature
     ```

2. **Run the scanner** (as Administrator):
   - The tool will scan all running processes
   - Progress is displayed in the console
   - Results are automatically saved to `results.txt`

3. **Review results**:
   - Open `results.txt` to see detected processes
   - Contains process name, PID, and creation date

## Output Format

The `results.txt` file contains:
```
Process Name | PID | Creation Date
============================================================
notepad.exe | 1234 | 2025-09-16 10:15:00
chrome.exe | 5678 | 2025-09-16 09:45:22
```

Only processes with string matches are listed.

## Building to Standalone Executable

### Prerequisites

1. **Install PyInstaller**:
   ```powershell
   pip install pyinstaller
   ```

### Build Commands

1. **Navigate to project directory**:
   ```powershell
   cd "path\to\stringfinder"
   ```

2. **Build executable with bundled resources**:
   ```powershell
   pyinstaller --onefile --console --add-data "xxstrings64.exe;." scanner.py
   ```

3. **Find your executable**:
   - Built executable: `dist\scanner.exe`
   - Completely standalone with `xxstrings64.exe` embedded
   - Still requires `strings.txt` in the same directory

## How It Works

1. **Process Enumeration**: Uses `psutil` to list all running processes
2. **String Extraction**: Runs `xxstrings64.exe -p <PID>` to extract strings from process memory
3. **Pattern Matching**: Compares extracted strings against patterns in `strings.txt`
4. **Results Recording**: Saves matching processes to `results.txt`
