import json
import datetime
from typing import Dict, Any
from call_scripts import PracticeAssistantVoiceEngine
from calls_logger import CallsLogger

class GovernedPracticeAssistant:
    def __init__(self, passport_path: str, company_name: str):
        with open(passport_path, 'r') as f:
            self.passport = json.load(f)
        
        self.company_name = company_name
        self.voice_engine = PracticeAssistantVoiceEngine(company_name, is_recording=True)
        self.logger = CallsLogger(retention_months=12)
        self.is_active = True
        self.call_count_today = 0

    def check_kill_switch(self) -> bool:
        """Simulates checking global kill-switch status (<3s target)."""
        return not self.is_active

    def process_inbound_call(self, caller_phone: str, caller_name: str, reason: str, requested_station: str):
        if self.check_kill_switch():
            raise RuntimeError("Agent execution halted by global Aurion Kill-Switch.")

        self.call_count_today += 1
        opening = self.voice_engine.get_disclosure_line()
        
        # Check vetting rule for station routing
        lane_a_result = self.voice_engine.handle_lane_a(caller_name, requested_station, is_first_call=True)
        
        if lane_a_result["status"] == "vetting_blocked":
            lane_b_result = self.voice_engine.handle_lane_b(
                caller_name, caller_phone, reason, promise_time="16:00 today"
            )
            log_record = self.logger.create_call_record(
                call_count_today=self.call_count_today,
                direction="inbound",
                lane="Lane B",
                caller_name=caller_name,
                caller_phone=caller_phone,
                reason=reason,
                disposition="message_taken",
                assigned_to=requested_station,
                promised_action=lane_b_result["captured_data"]["promised_action"],
                disclosure_given=True,
                recording_notice_given=True
            )
            return lane_b_result["spoken_response"], log_record

        return lane_a_result["spoken_response"], None
