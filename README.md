# CYB333 Midterm - Socket & Port Scanner

This repository contains three Python scripts for the CYB333 midterm assignment:

* server.py - simple TCP echo server (single-client)
* client.py - simple TCP client to interact with the server
* port_scanner.py - a safe TCP port scanner (only scans localhost and scanme.nmap.org)

All scripts include comments, error handling, and timestamped output suitable for screenshot evidence.

## Files

* **server.py**: runs a server that listens for a single client, echoes messages, and supports a `quit` command.
* **client.py**: connects to the server and interactively sends messages, or uses `--message` for one-shot mode.
* **port_scanner.py**: scans specified ports/ranges on allowed hosts with concurrency and delay options, and labels the service name of open ports.

## Usage examples

1. Start the server (terminal A):
python server.py --host 127.0.0.1 --port 65432

2. Start the client (terminal B):
python client.py --host 127.0.0.1 --port 65432

* In the client prompt, type a message and press Enter.
* Type `quit` to ask the server to close the connection.

3. One-shot client message:
python client.py --host 127.0.0.1 --port 65432 --message "Hello from one-shot"

4. Run the port scanner (examples):
python port_scanner.py --host 127.0.0.1 --ports 22,80,443 --timeout 0.3 --delay 0.01

python port_scanner.py --host 127.0.0.1 --ports 20-1024 --timeout 0.2 --delay 0.01 --workers 10

python port_scanner.py --host scanme.nmap.org --ports 79-82 --timeout 0.5 --delay 0.02 --workers 10

**Important:** for this assignment only scan `127.0.0.1` or `scanme.nmap.org`. The scanner enforces this and aborts on any other host.

## Test & Screenshot checklist

Include terminal screenshots showing:

* Server running and listening (timestamped line)
* Client connecting successfully and exchanging messages
* Client and server logs showing message exchange and graceful disconnection
* Client error when the server is not running (Connection refused)
* Port scanner output showing open/closed ports and the final summary
* Port scanner error handling for invalid ports or disallowed hosts

## Notes

* Requires Python 3.10+ (the client uses `str | None` type-hint syntax)
* Use the `--timeout`, `--delay`, and `--workers` flags on the scanner to tune performance and avoid aggressive scanning

## License

This code is provided for educational use in the CYB333 midterm only. Do not use it for unauthorized scanning.
