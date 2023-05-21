#!/usr/bin/env python3

import argparse
import pyfiglet
import colorama
import httpx
import threading
import time

def print_colored_message(message, color, font="slant"):
    ascii_art = pyfiglet.figlet_format(message, font=font)
    colored_ascii_art = f"{color}{ascii_art}{colorama.Style.RESET_ALL}"
    print(colored_ascii_art)

def check_response_time(url, method, headers, proxy, timeout):
    with httpx.Client(proxies=proxy, timeout=timeout, verify=False) as client:
        if method == 'POST':
            response = client.post(url, headers=headers)
        else:
            response = client.get(url, headers=headers)
        return response.elapsed.total_seconds(), response.status_code

def process_url(url, semaphore, method, headers, proxy, timeout):
    # Acquire semaphore to control the number of threads
    semaphore.acquire()

    # Check URL response time
    response_time, status_code = check_response_time(url, method, headers, proxy, timeout)
    if response_time > 10:
        print(f'URL: {url}')
        print(f'Method: {method}')
        print(f'Headers: {headers}')
        print(f'Proxy: {proxy}')
        print(f'Response Time: {response_time:.2f} seconds')
        print(f'Status Code: {status_code}')
        print('---')

    # Release semaphore to allow new threads to execute
    semaphore.release()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='URL Response Time Checker')
    parser.add_argument('-l', '--urls-file', dest='urls_file', metavar='FILE', required=True, help='Path to the file containing the URLs')
    parser.add_argument('-H', '--header', dest='headers', action='append', metavar='HEADER', help='Headers to be added to the request')
    parser.add_argument('--method', dest='method', choices=['GET', 'POST'], default='GET', help='HTTP method to be used for the request')
    parser.add_argument('-proxy', dest='proxy', metavar='PROXY', help='Proxy to be used for the request')
    parser.add_argument('-t', '--threads', dest='threads', type=int, default=10, help='Number of threads')
    parser.add_argument('--timeout', dest='timeout', type=int, default=10, help='Timeout in seconds')
    parser.add_argument('-d', '--delay', dest='delay', type=float, default=0, help='Delay between requests in seconds')
    args = parser.parse_args()

    # Print banner
    print_colored_message('Your program is running!', colorama.Fore.GREEN, font='starwars')

    # Extract command line arguments
    urls_file = args.urls_file
    headers = {header.split(":")[0].strip(): ":".join(header.split(":")[1:]).strip() for header in args.headers} if args.headers else {}
    method = args.method
    proxy = args.proxy
    num_threads = args.threads
    timeout = args.timeout
    delay = args.delay

    # Read URLs from file
    with open(urls_file, 'r') as file:
        urls = file.read().splitlines()

    # Create semaphore to control the number of threads
    semaphore = threading.BoundedSemaphore(value=num_threads)

    # Create threads for each URL
    threads = []
    for url in urls:
        t = threading.Thread(target=process_url, args=(url, semaphore, method, headers, proxy, timeout))
        t.start()
        threads.append(t)

        # Delay between requests
        time.sleep(delay)

    # Wait for all threads to finish
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

