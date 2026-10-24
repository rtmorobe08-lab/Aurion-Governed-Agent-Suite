import re
from typing import Dict, Any, List

class CustomerCareSupportEngine:
    def __init__(self, escalation_keywords: List[str] = None):
        self.escalation_keywords = escalation_keywords or ["LEGAL", "COMPLAINT", "POPIA_REQUEST", "REFUND_CLAIM"]

    def sanitize_input(self, text: str) -> str:
        """Redacts SA ID numbers and payment card patterns for POPIA compliance."""
        # Redact 13-digit SA ID numbers
        sanitized = re.sub(r'\b\d{13}\b', '[REDACTED_SA_ID]', text)
        # Redact 16-digit card patterns
        sanitized = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[REDACTED_CARD]', sanitized)
        return sanitized

    def evaluate_intent(self, user_message: str) -> Dict[str, Any]:
        """Evaluates customer message for tier-1 handling vs human escalation."""
        sanitized_msg = self.sanitize_input(user_message)
        upper_msg = sanitized_msg.upper()

        for kw in self.escalation_keywords:
            if kw in upper_msg:
                return {
                    "action": "ESCALATE_TO_HUMAN",
                    "reason": f"Escalation keyword detected: {kw}",
                    "sanitized_message": sanitized_msg,
                    "response": "Thank you for getting in touch. Your query has been flagged for our senior support team, and an agent will contact you shortly."
                }

        return {
            "action": "RESOLVE_TIER_1",
            "reason": "Standard enquiry",
            "sanitized_message": sanitized_msg,
            "response": "Thank you for reaching out. We have logged your request and are processing it within our standard service window."
        }
