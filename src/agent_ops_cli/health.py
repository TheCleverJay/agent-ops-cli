"""HTTP + optional local TCP port health probe."""
from __future__ import annotations

import argparse
import socket
import sys
import urllib.error
import urllib.request


def probe_http(url: str, timeout: float = 15.0) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        return False, f"FAIL http 000  {url} ({e})"
    ok = (200 <= code < 300) or code in (401, 403)
    return ok, f"{'OK' if ok else 'FAIL'}  http {code}  {url}"


def probe_port(port: int, host: str = "127.0.0.1", timeout: float = 2.0) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, f"OK  port :{port} listening"
    except OSError:
        return False, f"FAIL port :{port} closed"


def cmd_health(args: argparse.Namespace) -> int:
    ok = fail = 0
    good, msg = probe_http(args.url, args.timeout)
    print(msg)
    ok += int(good)
    fail += int(not good)
    if args.port is not None:
        good, msg = probe_port(args.port)
        print(msg)
        ok += int(good)
        fail += int(not good)
    print(f"summary ok={ok} fail={fail}")
    return 0 if fail == 0 else 1
