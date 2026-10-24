import datetime
from typing import Dict, Any, List

class CallsLogger:
    def __init__(self, retention_months: int = 12):
        self.retention_months = retention_months

    def create_call_record(
        self,
        call_count_today: int,
        direction: str,
        lane: str,
        caller_name: str,
        caller_phone: str,
        reason: str,
        disposition: str,
        assigned_to: str,
        promised_action: str,
        disclosure_given: bool = True,
        recording_notice_given: bool = True
    ) -> Dict[str, Any]:
        """Creates a standardized call log record according to Piece 3 schema."""
        now = datetime.datetime.now(datetime.timezone.utc)
        retention_date = now + datetime.timedelta(days=30 * self.retention_months)

        return {
            "call_id": f"CALL-{now.strftime('%Y%m%d')}-{call_count_today:03d}",
            "timestamp": now.isoformat(),
            "direction": direction,
            "lane": lane,
            "caller_name": caller_name,
            "caller_phone": caller_phone,
            "caller_company": "",
            "reason_for_call": reason,
            "kb_topics_used": [],
            "disposition": disposition,
            "assigned_to": assigned_to,
            "promised_action": promised_action,
            "followup_due": (now + datetime.timedelta(hours=4)).isoformat(),
            "ingestion_status": "logged",
            "disclosure_given": disclosure_given,
            "recording_notice_given": recording_notice_given,
            "retention_until": retention_date.strftime("%Y-%m-%d"),
            "register_entry_id": None
        }

    def generate_weekly_report_summary(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates the Monday 07:00 executive summary report."""
        return {
            "total_calls_handled": len(records),
            "promises_kept_vs_overdue": {
                "closed_on_time": sum(1 for r in records if r["ingestion_status"] == "closed"),
                "in_progress": sum(1 for r in records if r["ingestion_status"] == "in_progress"),
                "overdue": sum(1 for r in records if r["ingestion_status"] == "logged")
            },
            "leads_captured": [
                {"name": r["caller_name"], "phone": r["caller_phone"], "reason": r["reason_for_call"]}
                for r in records if r["caller_phone"]
            ]
        }
