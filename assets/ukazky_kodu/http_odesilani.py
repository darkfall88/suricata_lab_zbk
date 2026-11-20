    for index, case in enumerate(CASES, start=1):
        target = f"/?rid={token}&labcase={case.name}{case.suffix}"
        started = stamp()
        begun = time.perf_counter()
        outcome = "UNKNOWN"
        status = None
        error = None
        src_port = None
        # http.client sends supplied path as an HTTP/1.1 request-target;
        # it does not silently perform a second URL encoding pass.
        conn = http.client.HTTPConnection(args.target, args.port, timeout=args.timeout)
        try:
            conn.connect()
            if conn.sock is not None:
                src_port = conn.sock.getsockname()[1]
            headers = {"User-Agent": "Suricata-Advanced-Lab/2.0", "Connection": "close"}
            if case.content_type:
                headers["Content-Type"] = case.content_type
            conn.request(case.method, target, body=case.body.encode("utf-8") if case.method == "POST" else None, headers=headers)
            response = conn.getresponse()
            status = response.status
            response.read(32768)
            outcome = "HTTP_RESPONSE"
        except (socket.timeout, TimeoutError):
            outcome = "TIMEOUT"
        except (OSError, http.client.HTTPException) as exc:
            outcome = "NETWORK_ERROR"
            error = type(exc).__name__ + ": " + str(exc)
        finally:
            conn.close()
