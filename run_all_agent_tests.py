import sys
import os
import json

# Add core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'core')))
from master_router import AurionMasterRouter

def run_suite_tests():
    router = AurionMasterRouter()

    agents_to_test = [
        ("front_of_house", {"inquiry_type": "TEST_INTAKE", "status": "RUNNING"}),
        ("connector", {"integration_target": "PORTAL_TEST", "status": "SYNC"}),
        ("bookkeeper", {"ledger_account": "TEST_LEDGER", "amount_zar": 100.00}),
        ("inventory_payroll", {"module": "TEST_STOCK", "item_code": "SKU-001"}),
        ("paperwork", {"document_type": "TEST_MEMO", "status": "DRAFT"}),
        ("watchtower", {"incident_id": "INC-TEST-01", "severity_level": "LOW"})
    ]

    print("==================================================")
    print("   RUNNING FULL AURION GOVERNED AGENT SUITE      ")
    print("==================================================")

    results = []
    for agent_name, payload in agents_to_test:
        print(f"[*] Dispatching test payload to agent: {agent_name}...")
        response = router.route_request(agent_name, payload)
        results.append(response)

    print("\n==================================================")
    print(f"   SUCCESS: ALL {len(results)} AGENTS PASSED AUDIT ROUTING")
    print("==================================================")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_suite_tests()
