import json
from typing import Dict, Any, List

class BookkeeperReconciler:
    def __init__(self, vat_rate: float = 0.15, approval_threshold: float = 1000.00):
        self.vat_rate = vat_rate
        self.approval_threshold = approval_threshold

    def calculate_vat_breakdown(self, gross_amount: float) -> Dict[str, float]:
        """Calculates net amount and 15% VAT for South African SARS compliance."""
        net_amount = round(gross_amount / (1 + self.vat_rate), 2)
        vat_amount = round(gross_amount - net_amount, 2)
        return {
            "gross_amount": round(gross_amount, 2),
            "net_amount": net_amount,
            "vat_amount": vat_amount
        }

    def process_invoice_entry(self, vendor: str, invoice_number: str, gross_amount: float) -> Dict[str, Any]:
        """Processes an invoice entry and determines if human sign-off is required."""
        breakdown = self.calculate_vat_breakdown(gross_amount)
        requires_approval = gross_amount >= self.approval_threshold

        return {
            "vendor": vendor,
            "invoice_number": invoice_number,
            "financial_breakdown": breakdown,
            "status": "pending_owner_approval" if requires_approval else "auto_reconciled",
            "human_approval_required": requires_approval
        }
