#!/usr/bin/env python3
#Auther: Sadly Rem01x
import argparse
import requests
import threading
from queue import Queue
from termcolor import colored
import sys
# Define command line arguments
parser = argparse.ArgumentParser(description='SadBuster Directory Brute Forcer')
parser.add_argument('--url', required=True, help='Target URL')
parser.add_argument('--thread', default=10, type=int, help='Number of threads (default: 10)')
parser.add_argument('-w', '--wordlist', default='wordlist.txt', help='Wordlist path (default: wordlist.txt)')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
parser.add_argument('-o', '--output', help='Output file path')
parser.add_argument('-H', '--headers', nargs='*', help='Custom headers')
parser.add_argument('--no-https', action='store_true', help='Disable HTTPS')

# Show help if no arguments provided
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Parse command line arguments
args = parser.parse_args()

# Set URL and headers
url = args.url
headers = {}
if args.headers:
    for header in args.headers:
        key, value = header.split(':')
        headers[key.strip()] = value.strip()

# Check if HTTPS is enabled
if not args.no_https and not url.startswith('https://'):
    url = 'https://' + url

# Load wordlist
with open(args.wordlist) as f:
    wordlist = [line.strip() for line in f]

# Define a function to make requests
def make_request(url, path):
    try:
        r = requests.get(url + path, headers=headers)
        if r.status_code == 200 or r.status_code == 301 or r.status_code == 302:
            output = f"{colored(str(r.status_code), 'green')} {url+path}"
            print(output)
            if args.output:
                with open(args.output, 'a') as f:
                    f.write(output + '\n')
        elif args.verbose:
            print(f"{colored(str(r.status_code), 'red')} {url+path}")
    except requests.exceptions.RequestException:
        if args.verbose:
                    pass
# Define a function to process the queue
def process_queue():
    while True:
        path = queue.get()
        make_request(url, path)
        queue.task_done()

# Create a queue and start the threads
queue = Queue()
for i in range(args.thread):
    t = threading.Thread(target=process_queue)
    t.daemon = True
    t.start()

# Add paths to the queue
for path in wordlist:
    queue.put(path)

# Wait for the queue to be processed
queue.join()
