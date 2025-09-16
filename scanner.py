import psutil
import subprocess
import os
import sys
import tempfile
from datetime import datetime
from typing import List, Dict
from pathlib import Path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_xxstrings_exe_path():
    exe_name = "xxstrings64.exe"
    src_path = resource_path(exe_name)
    temp_dir = tempfile.gettempdir()
    dst_path = os.path.join(temp_dir, exe_name)
    try:
        if not os.path.exists(dst_path) or (os.path.getsize(dst_path) != os.path.getsize(src_path)):
            with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
                dst.write(src.read())
    except Exception:
        pass
    return dst_path

class ProcessScanner:
    def __init__(self, strings_file: str = "strings.txt", output_file: str = "results.txt"):
        self.strings_file = strings_file
        self.output_file = output_file
        self.processes_info = []
        self.search_strings = []

    def count_processes(self) -> int:
        try:
            return len(list(psutil.process_iter()))
        except Exception:
            return 0

    def get_process_memory(self, pid: int) -> str:
        try:
            process = psutil.Process(pid)
            memory_mb = process.memory_info().rss / 1024 / 1024
            return f"{memory_mb:.2f} MB"
        except Exception:
            return "Unknown"

    def get_process_details(self, pid: int) -> Dict:
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'memory': self.get_process_memory(pid),
                'cpu_percent': process.cpu_percent(),
                'status': process.status(),
                'created_time': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                'username': process.username()
            }
        except Exception:
            return None

    def collect_processes_info(self):
        self.processes_info = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_info = self.get_process_details(proc.info['pid'])
                if process_info:
                    self.processes_info.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def load_search_strings(self) -> bool:
        if not os.path.exists(self.strings_file):
            return False
        with open(self.strings_file, "r", encoding='utf-8') as file:
            self.search_strings = [line.strip() for line in file.readlines() if line.strip()]
        return True

    def scan_process(self, process: Dict) -> List[str]:
        found_strings = []
        try:
            exe_path = get_xxstrings_exe_path()
            command = f'"{exe_path}" -p {process["pid"]}'
            subproc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output, error = subproc.communicate(timeout=10)

            for search_string in self.search_strings:
                if search_string in output:
                    found_strings.append(search_string)

        except subprocess.TimeoutExpired:
            subproc.kill()
        except Exception:
            pass

        return found_strings

    def write_results(self, results: List[Dict]):
        # Always overwrite results.txt
        with open(self.output_file, "w", encoding='utf-8') as file:
            file.write("Process Name | PID | Creation Date\n")
            file.write("=" * 60 + "\n")

            for result in results:
                process = result['process']
                name = process['name']
                pid = process['pid']
                created_time = process['created_time']

                file.write(f"{name} | {pid} | {created_time}\n")

    def run(self):
        print("Process Scanner Starting...")

        process_count = self.count_processes()
        print(f"Found {process_count} running processes")

        if not self.load_search_strings():
            print("Error loading search strings.")
            return

        print("Collecting process information...")
        self.collect_processes_info()
        print(f"Collected information for {len(self.processes_info)} processes")

        print("\nScanning processes for strings...")
        results = []
        for i, process in enumerate(self.processes_info, 1):
            print(f"Scanning process {i}/{len(self.processes_info)}: {process['name']} (PID: {process['pid']})")
            found_strings = self.scan_process(process)
            if found_strings:
                results.append({
                    'process': process,
                    'strings': found_strings
                })

        if results:
            print(f"\nFound matches in {len(results)} processes")
            self.write_results(results)
            print(f"Results written to {self.output_file}")
        else:
            print("\nNo matches found in any process")

if __name__ == "__main__":
    scanner = ProcessScanner()
    scanner.run()
