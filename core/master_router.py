import json
import datetime

class AurionMasterRouter:
    def __init__(self):
        self.active_agents = [
            "front_of_house",
            "connector",
            "bookkeeper",
            "inventory_payroll",
            "paperwork",
            "watchtower"
        ]

    def route_request(self, agent_name: str, payload: dict) -> dict:
        if agent_name not in self.active_agents:
            raise ValueError(f"Agent '{agent_name}' is not recognized in the Aurion Governance Suite.")

        # Wrap payload with standard compliance envelope
        dispatch_packet = {
            "routed_to": agent_name,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "status": "DISPATCHED_SUCCESS",
            "payload": payload
        }
        return dispatch_packet

if __name__ == "__main__":
    router = AurionMasterRouter()
    test_payload = {"task": "Verify transaction ledger", "amount_zar": 15000.00}
    result = router.route_request("bookkeeper", test_payload)
    print(json.dumps(result, indent=2))
