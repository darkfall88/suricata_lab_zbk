def match_event(event: dict[str, Any], row: dict[str, Any], margin: float) -> tuple[int, float] | None:
    if event.get("src_ip") != row["source"] or event.get("dest_ip") != row["target"] or event.get("dest_port") != row["port"]:
        return None
    try:
        t = read_stamp(event["timestamp"])
        start, end = read_stamp(row["started"]), read_stamp(row["ended"])
    except (ValueError, KeyError):
        return None
    if not start - timedelta(seconds=margin) <= t <= end + timedelta(seconds=margin):
        return None
    path = str((event.get("http") or {}).get("url") or "")
    query = parse_qs(urlsplit(path).query, keep_blank_values=True)
    tagged_case = query.get("labcase", [None])[0]
    tagged_run = query.get("rid", [None])[0]
    has_token = tagged_case == row["case"] and tagged_run == row["run_id"]
    # A URL containing explicit tags for ANOTHER test is never a match.
    if tagged_case is not None and not has_token:
        return None
    port_matches = event.get("src_port") == row.get("source_port") and row.get("source_port") is not None
    if not has_token and not port_matches:
        return None
    seconds = abs((t - start).total_seconds())
    return (0 if has_token else 1, seconds)
