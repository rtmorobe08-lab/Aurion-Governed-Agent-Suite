import json
from support_engine import CustomerCareSupportEngine
from logger import CustomerCareAuditLogger

class GovernedCustomerCareAgent:
    def __init__(self, passport_path: str):
        with open(passport_path, 'r') as f:
            self.passport = json.load(f)

        self.agent_id = self.passport.get("agent_id", "AGENT-03-GOVERNED-CUSTOMER-CARE")
        self.engine = CustomerCareSupportEngine()
        self.logger = CustomerCareAuditLogger()
        self.is_active = True

    def process_incoming_message(self, channel: str, user_message: str):
        if not self.is_active:
            raise RuntimeError("Agent execution halted by global Aurion Kill-Switch.")

        eval_result = self.engine.evaluate_intent(user_message)
        audit_entry = self.logger.log_interaction(self.agent_id, channel, eval_result)

        return {
            "reply": eval_result["response"],
            "action_type": eval_result["action"],
            "audit": audit_entry
        }
