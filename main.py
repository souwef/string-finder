import psutil
import subprocess

def count_processes():
    process_count = psutil.process_iter()
    return sum(1 for _ in process_count)

process_quant = count_processes()
print(f"Loaded {process_quant} processes")

processes_info = []
for proc in psutil.process_iter(['pid', 'name']):
    process_info = {'pid': proc.info['pid'], 'name': proc.info['name']}
    processes_info.append(process_info)

output_file = "found_strings.txt"
with open("strings.txt", "r") as search_file:
    search_strings = search_file.readlines()
    search_strings = [string.strip() for string in search_strings if string.strip()]

with open(output_file, "w") as output_file:
    for process in processes_info:
        command = f"xxstrings64.exe -p {process['pid']}"
        subproc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = subproc.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        for search_string in search_strings:
            search_string = search_string.strip()
            if search_string in output:
                output_file.write(f"\"{process['name']}\" - \"{process['pid']}\"\n")
                output_file.write(f"\"{search_string}\"\n")
                output_file.write("----------------------------------------------\n")

print("Search results written to found_strings.txt")