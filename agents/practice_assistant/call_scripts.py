import datetime
from typing import Dict, Any, Optional

class PracticeAssistantVoiceEngine:
    def __init__(self, company_name: str, is_recording: bool = False):
        self.company_name = company_name
        self.is_recording = is_recording

    def get_disclosure_line(self) -> str:
        """Mandatory opening line for every call."""
        base_line = f"Thank you for calling {self.company_name}, you're speaking with the office assistant. How can I help you today?"
        if self.is_recording:
            base_line += " Just to let you know, this call may be recorded for quality and record-keeping."
        return base_line

    def handle_lane_a(self, caller_name: str, station: str, is_first_call: bool) -> Dict[str, Any]:
        """Lane A: Answered Call & Warm Transfer (with vetting rule)."""
        if is_first_call and station in ["Senior Partner", "Principal"]:
            # Vetting Rule: Block direct transfer on first call; route to Lane B
            return {
                "status": "vetting_blocked",
                "spoken_response": f"I'm afraid {station} is not available right now, but I can take your details and ensure they call you back.",
                "action": "switch_to_lane_b"
            }
        return {
            "status": "transfer_initiated",
            "spoken_response": f"May I ask who's calling? Thank you, {caller_name}. I'll put you through to {station} right away.",
            "action": "warm_transfer"
        }

    def handle_lane_b(self, caller_name: str, phone: str, reason: str, promise_time: str) -> Dict[str, Any]:
        """Lane B: Person Not Available (Capture, Engage, Promise)."""
        response_text = (
            f"Here's what happens next, {caller_name}: our team will call you back before {promise_time}. "
            "You have my word on it and it's logged, so it won't be forgotten."
        )
        return {
            "status": "promise_logged",
            "spoken_response": response_text,
            "captured_data": {
                "caller_name": caller_name,
                "caller_phone": phone,
                "reason_for_call": reason,
                "promised_action": f"Callback before {promise_time}"
            }
        }

    def handle_lane_d_callback(self, missed_number: str) -> str:
        """Lane D: Missed-Call Automatic Callback Loop."""
        return (
            f"Hello, this is the office assistant at {self.company_name} — "
            f"I see we missed your call earlier, and I wanted to make sure we didn't leave you waiting. How can I help?"
        )
