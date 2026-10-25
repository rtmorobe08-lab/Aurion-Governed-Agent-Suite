import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_bookkeeper_entry():
    router = AurionMasterRouter()

    # Simulate a financial ledger verification payload
    bookkeeper_payload = {
        "ledger_account": "SMME_TRADE_FINANCE",
        "transaction_type": "DEBIT_ALLOCATION",
        "amount_zar": 25000.00,
        "audit_status": "VERIFIED_COMPLIANT"
    }

    # Route through master compliance router
    response = router.route_request("bookkeeper", bookkeeper_payload)

    print("--- BOOKKEEPER AGENT AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_bookkeeper_entry()
