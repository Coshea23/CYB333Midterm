#!/usr/bin/env python3
"""
Simple TCP echo server.

Usage:
    python server.py --host 127.0.0.1 --port 65432

The server listens for one client at a time, echoes messages and responds with an acknowledgement.
Type Ctrl+C in the server terminal to shutdown gracefully.
"""
import argparse
import socket
import sys
import time
from typing import Tuple

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432
BUFFER_SIZE = 4096


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Handle a connected client: receive messages and reply until client disconnects."""
    print(f"[{timestamp()}] Connected by {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    # Client closed connection
                    print(f"[{timestamp()}] Connection closed by {addr}")
                    break
                message = data.decode(errors="replace").strip()
                print(f"[{timestamp()}] Received from {addr}: {message!r}")
                if message.lower() in {"quit", "exit"}:
                    reply = "Server: Goodbye. Closing connection."
                    conn.sendall(reply.encode())
                    print(f"[{timestamp()}] Closing connection with {addr} on client request.")
                    break
                # Echo with acknowledgement
                reply = f"Server ACK ({timestamp()}): Received {len(message)} bytes: {message}"
                conn.sendall(reply.encode())
    except Exception as exc:
        print(f"[{timestamp()}] Error while handling client {addr}: {exc}")


def run_server(host: str, port: int) -> None:
    """Start the TCP server and accept connections."""
    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Allow reuse of address/port
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            print(f"[{timestamp()}] Server listening on {host}:{port}")
            while True:
                try:
                    conn, addr = s.accept()
                except KeyboardInterrupt:
                    print(f"\n[{timestamp()}] KeyboardInterrupt received. Shutting down server.")
                    break
                except Exception as exc:
                    print(f"[{timestamp()}] Accept failed: {exc}")
                    continue
                # Handle client connection
                handle_client(conn, addr)
    except PermissionError:
        print(f"[{timestamp()}] Permission denied binding to {host}:{port}. Try a higher port.")
    except OSError as oe:
        print(f"[{timestamp()}] OS error when starting server: {oe}")
    except Exception as exc:
        print(f"[{timestamp()}] Unexpected server error: {exc}")
    finally:
        print(f"[{timestamp()}] Server exiting.")


def parse_args():
    p = argparse.ArgumentParser(description="Simple TCP echo server.")
    p.add_argument("--host", default=DEFAULT_HOST, help="Host to bind to (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to bind to (default: {DEFAULT_PORT})")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not (1 <= args.port <= 65535):
        print(f"[{timestamp()}] Invalid port: {args.port}. Must be between 1 and 65535.", file=sys.stderr)
        sys.exit(2)
    run_server(args.host, args.port)
