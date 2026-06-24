#!/usr/bin/env python3
"""
Simple TCP client to interact with the server.

Usage:
    python client.py --host 127.0.0.1 --port 65432

Interactive mode:
    - Type a message and press Enter to send
    - Type 'quit' or 'exit' to ask the server to close the connection and then exit
"""
import argparse
import socket
import sys
import time

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432
BUFFER_SIZE = 4096


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def run_client(host: str, port: int, one_shot_message: str | None = None) -> None:
    """Connect to the server and either send one_shot_message or enter interactive mode."""
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            print(f"[{timestamp()}] Connected to {host}:{port}")
            if one_shot_message is not None:
                sock.sendall(one_shot_message.encode())
                data = sock.recv(BUFFER_SIZE)
                print(f"[{timestamp()}] Server replied: {data.decode(errors='replace')}")
                return
            # Interactive loop
            while True:
                try:
                    msg = input("Enter message (or 'quit' to exit): ").strip()
                except EOFError:
                    print("\nEOF received. Disconnecting.")
                    break
                if not msg:
                    continue
                try:
                    sock.sendall(msg.encode())
                except BrokenPipeError:
                    print(f"[{timestamp()}] Connection broken while sending. Exiting.")
                    break
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    print(f"[{timestamp()}] Server closed connection.")
                    break
                print(f"[{timestamp()}] Server: {data.decode(errors='replace')}")
                if msg.lower() in {"quit", "exit"}:
                    print(f"[{timestamp()}] Requested server close. Exiting.")
                    break
    except ConnectionRefusedError:
        print(f"[{timestamp()}] Connection refused: is the server running on {host}:{port}?", file=sys.stderr)
    except socket.timeout:
        print(f"[{timestamp()}] Connection timed out connecting to {host}:{port}", file=sys.stderr)
    except socket.gaierror:
        print(f"[{timestamp()}] DNS error: could not resolve host {host}", file=sys.stderr)
    except Exception as exc:
        print(f"[{timestamp()}] Unexpected client error: {exc}", file=sys.stderr)


def parse_args():
    p = argparse.ArgumentParser(description="Simple TCP client for testing the echo server.")
    p.add_argument("--host", default=DEFAULT_HOST, help="Server host (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Server port (default: {DEFAULT_PORT})")
    p.add_argument("--message", "-m", help="Send a single message and exit (one-shot mode).")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not (1 <= args.port <= 65535):
        print(f"[{timestamp()}] Invalid port: {args.port}. Must be between 1 and 65535.", file=sys.stderr)
        sys.exit(2)
    run_client(args.host, args.port, args.message)
