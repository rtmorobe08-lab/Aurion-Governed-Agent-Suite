import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_connector_dispatch():
    router = AurionMasterRouter()

    # Simulate an external API integration sync payload
    connector_payload = {
        "integration_target": "GOV_PROCUREMENT_PORTAL",
        "sync_status": "ACTIVE",
        "payload_packets_transferred": 14,
        "authentication_verified": True
    }

    # Route through master compliance router
    response = router.route_request("connector", connector_payload)

    print("--- CONNECTOR AGENT AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_connector_dispatch()
