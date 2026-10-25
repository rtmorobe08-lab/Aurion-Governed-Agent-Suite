import sys
import os
import json

# Add core directory to path to import router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../core')))
from master_router import AurionMasterRouter

def simulate_inventory_payroll():
    router = AurionMasterRouter()

    # Simulate an inventory threshold or payroll allocation payload
    payload = {
        "module": "INVENTORY_THRESHOLD",
        "item_code": "SPAZA_TRADE_KIT_01",
        "stock_level": 42,
        "status": "OPTIMAL"
    }

    # Route through master compliance router
    response = router.route_request("inventory_payroll", payload)

    print("--- INVENTORY & PAYROLL AGENT AUDIT EVENT ---")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    simulate_inventory_payroll()
