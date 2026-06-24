#!/usr/bin/env python3
"""
Simple TCP port scanner.

Usage examples:
    python port_scanner.py --host 127.0.0.1 --ports 22,80,443
    python port_scanner.py --host 127.0.0.1 --ports 20-1024 --timeout 0.3 --delay 0.01 --workers 50
    python port_scanner.py --host scanme.nmap.org --ports 79-82

Notes and safety:
    - Only scan localhost (127.0.0.1) or scanme.nmap.org for this assignment.
    - Use small concurrency and delays to avoid aggressive scanning.
"""
import argparse
import concurrent.futures
import socket
import sys
import time
from typing import Iterable, List, Tuple

DEFAULT_TIMEOUT = 0.5
DEFAULT_DELAY = 0.01
DEFAULT_WORKERS = 10


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def parse_ports(ports_str: str) -> List[int]:
    """Parse a ports specification like '22,80,443,1000-1010' into a sorted list of ints."""
    ports = set()
    for part in ports_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                a_i = int(a)
                b_i = int(b)
            except ValueError:
                raise ValueError(f"Invalid port range: {part}")
            if a_i > b_i:
                a_i, b_i = b_i, a_i
            for p in range(a_i, b_i + 1):
                ports.add(p)
        else:
            try:
                ports.add(int(part))
            except ValueError:
                raise ValueError(f"Invalid port value: {part}")
    # Validate ports
    validated = [p for p in ports if 1 <= p <= 65535]
    invalid = set(ports) - set(validated)
    if invalid:
        raise ValueError(f"Ports out of range (1-65535): {sorted(invalid)}")
    return sorted(validated)


def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool, str]:
    """Return (port, is_open, error_message)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # connect_ex returns 0 on success, error code otherwise
            res = s.connect_ex((host, port))
            if res == 0:
                return port, True, ""
            else:
                return port, False, f"connect_ex={res}"
    except socket.gaierror:
        return port, False, "Name resolution failure"
    except Exception as exc:
        return port, False, f"Error: {exc}"


def run_scan(host: str, ports: Iterable[int], timeout: float, delay: float, workers: int) -> None:
    ports = list(ports)
    print(f"[{timestamp()}] Starting scan on host={host} for {len(ports)} ports (timeout={timeout}s, delay={delay}s, workers={workers})")
    start = time.time()
    open_ports: List[int] = []
    results = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit tasks
            future_to_port = {executor.submit(scan_port, host, port, timeout): port for port in ports}
            for fut in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[fut]
                try:
                    p, is_open, msg = fut.result()
                except Exception as exc:
                    print(f"[{timestamp()}] Port {port}: Exception {exc}")
                    continue
                if is_open:
                    # Look up the well-known service name for this port (e.g. 22 -> ssh).
                    try:
                        service = socket.getservbyport(p)
                    except OSError:
                        service = "unknown"
                    print(f"[{timestamp()}] Port {p}: OPEN ({service})")
                    open_ports.append(p)
                else:
                    print(f"[{timestamp()}] Port {p}: closed ({msg})")
                results.append((p, is_open, msg))
                # rate-limiting delay
                if delay:
                    time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n[{timestamp()}] Scan interrupted by user.")
    except socket.gaierror:
        print(f"[{timestamp()}] Host resolution error: cannot resolve {host}")
    except Exception as exc:
        print(f"[{timestamp()}] Unexpected scanning error: {exc}")
    finally:
        elapsed = time.time() - start
        print(f"[{timestamp()}] Scan finished in {elapsed:.2f} seconds. Open ports: {sorted(open_ports)}")


def parse_args():
    p = argparse.ArgumentParser(description="Simple TCP port scanner (safe defaults).")
    p.add_argument("--host", required=True, help="Target host (use 127.0.0.1 or scanme.nmap.org for testing).")
    p.add_argument("--ports", required=True, help="Ports to scan: examples '22,80,443' or '20-1024' or mixed.")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"Socket timeout in seconds (default {DEFAULT_TIMEOUT})")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY, help=f"Delay between port checks in seconds (default {DEFAULT_DELAY})")
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"Number of concurrent workers (default {DEFAULT_WORKERS})")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        ports_list = parse_ports(args.ports)
    except ValueError as ve:
        print(f"[{timestamp()}] Port parsing error: {ve}", file=sys.stderr)
        sys.exit(2)
    # Safety: warn if host not allowed (we only permit localhost or scanme.nmap.org)
    allowed = {"127.0.0.1", "localhost", "scanme.nmap.org"}
    if args.host not in allowed:
        print(f"[{timestamp()}] WARNING: You have asked to scan {args.host}. For this assignment only scan localhost or scanme.nmap.org.", file=sys.stderr)
        print(f"[{timestamp()}] Aborting scan for safety.")
        sys.exit(3)
    run_scan(args.host, ports_list, args.timeout, args.delay, args.workers)
     
