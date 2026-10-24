import hashlib
import json
import datetime
from typing import Dict, Any

class CustomerCareAuditLogger:
    def __init__(self):
        self.logs = []

    def log_interaction(self, agent_id: str, channel: str, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an audit log entry for every customer interaction."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        payload = {
            "timestamp": timestamp,
            "agent_id": agent_id,
            "channel": channel,
            "action": evaluation_data.get("action"),
            "reason": evaluation_data.get("reason")
        }

        payload_string = json.dumps(payload, sort_keys=True)
        audit_log_hash = hashlib.sha256(payload_string.encode('utf-8')).hexdigest()

        log_entry = {
            "payload": payload,
            "audit_log_hash": audit_log_hash
        }
        self.logs.append(log_entry)
        return log_entry
