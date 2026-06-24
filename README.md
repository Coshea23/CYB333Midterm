# CYB333 Midterm - Socket & Port Scanner

This repository contains three Python scripts for the CYB333 midterm assignment:

- server.py - simple TCP echo server (single-client)
- client.py - simple TCP client to interact with the server
- port_scanner.py - a safe TCP port scanner (only scans localhost and scanme.nmap.org)

All scripts include comments, error handling, and timestamped output suitable for screenshot evidence.

## Files

- server.py: run a server that listens for a single client, echoes messages, and supports a `quit` command.
- client.py: connect to the server and interactively send messages or use `--message` for one-shot.
- port_scanner.py: scan specified ports/ranges on allowed hosts with concurrency and delay options.

## Usage examples

1. Start the server (terminal A):

```bash
python server.py --host 0.0.0.0 --port 65432
```

2. Start the client (terminal B):

```bash
python client.py --host 127.0.0.1 --port 65432
```

- In the client interactive prompt, type a message and press Enter.
- Type `quit` to request the server close the connection.

3. One-shot client message:

```bash
python client.py --host 127.0.0.1 --port 65432 --message "Hello from one-shot"
```

4. Run the port scanner (examples):

```bash
python port_scanner.py --host 127.0.0.1 --ports 22,80,443 --timeout 0.3 --delay 0.01
python port_scanner.py --host 127.0.0.1 --ports 20-1024 --timeout 0.2 --delay 0.005 --workers 100
python port_scanner.py --host scanme.nmap.org --ports 79-82 --timeout 0.5 --delay 0.02 --workers 20
```

Important: for the assignment only scan `127.0.0.1` or `scanme.nmap.org`.

## Test & Screenshot checklist

Include terminal screenshots showing:
- Server running and listening (timestamped line)
- Client connecting successfully and exchanging messages
- Client and server logs showing message exchange and graceful disconnection
- Client error when server is not running (Connection refused)
- Port scanner output showing open/closed ports and final summary
- Port scanner error handling for invalid ports or disallowed hosts

## Notes

- Requires Python 3.8+
- Use the `--timeout`, `--delay`, and `--workers` flags on the scanner to tune performance and avoid aggressive scanning.

## License

This code is provided for educational use in the CYB333 midterm only. Do not use for unauthorized scanning.
