import hashlib
import json
import datetime
from typing import Dict, Any

class BookkeeperAuditLogger:
    def __init__(self):
        self.log_chain = []

    def log_financial_action(self, agent_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Logs a financial decision and generates a cryptographic hash."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        payload = {
            "timestamp": timestamp,
            "agent_id": agent_id,
            "action_data": action_data
        }
        
        # Canonical JSON string for deterministic SHA-256 hash
        payload_string = json.dumps(payload, sort_keys=True)
        audit_log_hash = hashlib.sha256(payload_string.encode('utf-8')).hexdigest()
        
        log_entry = {
            "payload": payload,
            "audit_log_hash": audit_log_hash
        }
        self.log_chain.append(log_entry)
        return log_entry
