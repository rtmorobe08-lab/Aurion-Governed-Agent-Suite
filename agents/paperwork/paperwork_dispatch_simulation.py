import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_paperwork_dispatch():
    router = AurionMasterRouter()

    # Simulate a documentation generation or compliance briefing memo payload
    payload = {
        "document_type": "BRIEFING_MEMO_LOCALIZATION",
        "status": "DRAFT_GENERATED",
        "approval_tier": "EXECUTIVE_REVIEW",
        "compliance_standard": "POPIA_FICA"
    }

    # Route through master compliance router
    response = router.route_request("paperwork", payload)

    print("--- PAPERWORK AGENT AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_paperwork_dispatch()
