        action = best_pattern.get("alert", {}).get("action") if best_pattern else None
        seen = best_pattern is not None
        expected = row["expected_match"]
        if expected == "yes":
            coverage = "MATCH" if seen else "MISSING_EXPECTED"
        elif expected == "no":
            coverage = "UNEXPECTED_MATCH" if any(x[2].get("alert", {}).get("signature_id") != CONTROL_SID for x in candidates) else "CLEAN"
        else:
            coverage = "OBSERVED_MATCH" if seen else "OBSERVED_NO_MATCH"
        verdict = "UNVERIFIED"
        if seen:
            verdict = "BLOCKED" if action == "blocked" else ("ALLOWED_ALERT" if action == "allowed" else "UNKNOWN_ACTION")
