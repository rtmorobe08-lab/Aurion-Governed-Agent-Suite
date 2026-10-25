import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_watchtower_alert():
    router = AurionMasterRouter()

    # Simulate an incoming system anomaly or security flag caught by Watchtower
    alert_payload = {
        "incident_id": "INC-WATCHTOWER-2026-001",
        "severity_level": "HIGH",
        "description": "Unauthorized API boundary scan detected on connector gateway.",
        "human_gate_status": "PENDING_REVIEW"
    }

    # Route through master compliance router
    response = router.route_request("watchtower", alert_payload)

    print("--- WATCHTOWER AGENT AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_watchtower_alert()
