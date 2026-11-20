def attempt(target: str, port: int, phase: str, attempt_id: str,
            socket_timeout: float, run_start_mono: float,
            scheduled_offset_s: float) -> dict:
    start_mono = time.monotonic()
    started_at = now_utc()
    status, detail, source_port = "ERROR", "", None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(socket_timeout)
        try:
            s.connect((target, port))
            status = "OPEN"
        except ConnectionRefusedError:
            status = "CLOSED"
        except (TimeoutError, socket.timeout):
            status = "TIMEOUT"
        except OSError as exc:
            if exc.errno == errno.ETIMEDOUT:
                status = "TIMEOUT"
            else:
                detail = f"errno={exc.errno}: {exc.strerror}"
        try:
            local_port = s.getsockname()[1]
            source_port = local_port if local_port else None
        except OSError:
            pass
    return {
        "phase": phase, "attempt_id": attempt_id, "port": port,
        "source_port": source_port,
        "scheduled_offset_s": round(scheduled_offset_s, 6),
        "started_at": started_at,
        "started_offset_s": round(start_mono - run_start_mono, 6),
        "completed_at": now_utc(),
        "duration_ms": round((time.monotonic() - start_mono) * 1000, 2),
        "status": status, "detail": detail,
    }
