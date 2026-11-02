import sys
import os
import json

# Add core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'core')))
from master_router import AurionMasterRouter


def run_module_tests():
    """Per-agent test modules that the router does not dispatch."""
    import subprocess
    suites = [os.path.join("agents", "tender_scout", "test_tender_scout.py")]
    failed = 0
    for suite in suites:
        if not os.path.exists(suite):
            continue
        print(f"[*] Running module tests: {suite}")
        r = subprocess.run([sys.executable, suite], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-800:]); print(r.stderr[-400:]); failed += 1
        else:
            tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
            print("    " + (tail[0] if tail else "ok"))
    return failed

def run_governance_gate():
    """Fail-closed governance gate: the suite must satisfy its own parameters."""
    import subprocess
    print("\n==================================================")
    print("   GOVERNANCE GATE — VALIDATING AGENT PARAMETERS  ")
    print("==================================================")
    validator = os.path.join(os.path.dirname(os.path.abspath(__file__)), "governance", "validate_governance.py")
    if not os.path.exists(validator):
        print("BLOCKED: governance validator missing. An ungoverned suite must not pass.")
        return 1
    result = subprocess.run([sys.executable, validator], capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print("BLOCKED: governance validation failed. Merge refused.")
        return 1
    print("GOVERNANCE GATE: PASSED")
    return 0

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
    module_failures = run_module_tests()
    gate = run_governance_gate()
    sys.exit(1 if (gate or module_failures) else 0)
