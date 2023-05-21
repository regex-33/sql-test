#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--payloads_file", help="File containing list of payloads")
args = parser.parse_args()

if not args.payloads_file:
    print("Usage: python script.py -p <payloads_file>")
    exit(1)

output_file = "possible_sql.txt"

# Execute command: gf urls | sort -u | uro | gf sqli
command = "gf urls | sort -u | uro | gf sqli"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Check for errors
if error:
    print(f"Error: {error.decode().strip()}")
    exit(1)

# Read URLs from command output
urls = output.decode().splitlines()

# Read payloads from file
with open(args.payloads_file) as f:
    payloads = f.read().splitlines()

# Iterate over URLs
for url in urls:
    # Iterate over payloads
    for payload in payloads:
        command = f"echo {url} | ~/go/bin/qsreplace '{payload}'"
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        with open(output_file, "a") as f:
            f.write(output.stdout + "\n")
