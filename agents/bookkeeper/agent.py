import json
from reconciler import BookkeeperReconciler
from logger import BookkeeperAuditLogger

class GovernedBookkeeperAgent:
    def __init__(self, passport_path: str):
        with open(passport_path, 'r') as f:
            self.passport = json.load(f)

        self.agent_id = self.passport.get("agent_id", "AGENT-02-GOVERNED-BOOKKEEPER")
        self.approval_threshold = self.passport.get("single_transaction_approval_threshold_zar", 1000.00)
        self.reconciler = BookkeeperReconciler(vat_rate=0.15, approval_threshold=self.approval_threshold)
        self.logger = BookkeeperAuditLogger()
        self.is_active = True

    def run_invoice_reconciliation(self, vendor: str, invoice_number: str, amount_zar: float):
        if not self.is_active:
            raise RuntimeError("Agent execution halted by global Aurion Kill-Switch.")

        reconciliation_result = self.reconciler.process_invoice_entry(vendor, invoice_number, amount_zar)
        audit_record = self.logger.log_financial_action(self.agent_id, reconciliation_result)

        return {
            "result": reconciliation_result,
            "audit_trail": audit_record
        }
