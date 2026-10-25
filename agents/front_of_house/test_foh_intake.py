import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_foh_intake():
    router = AurionMasterRouter()

    # Simulate an incoming client inquiry or intake request at the front door
    intake_payload = {
        "client_id": "CLI-2026-9081",
        "inquiry_type": "SMME_PROCUREMENT_ADVOCACY",
        "urgency": "NORMAL",
        "message": "Requesting briefing memo on upcoming local localization compliance frameworks."
    }

    # Route through master compliance router
    response = router.route_request("front_of_house", intake_payload)

    print("--- FRONT OF HOUSE INTAKE AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_foh_intake()
