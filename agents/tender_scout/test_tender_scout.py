"""Governance and behaviour tests for Tender Scout."""
import os, sys, unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tender_scout_simulation import TenderScout, PermissionDenied


class TestTenderScout(unittest.TestCase):
    def setUp(self):
        self.s = TenderScout(
            capability_keywords=["civil works", "reinforcement steel", "fire services"],
            value_floor_zar=50_000, value_ceiling_zar=5_000_000, window_days=14,
            held_certifications=["CIDB 2CE"],
        )
        self.today = date(2026, 11, 2)

    def test_matching_notice_is_shortlisted(self):
        notices = [{"reference": "T1", "title": "Reinforcement steel supply",
                    "scope": "civil works and reinforcement steel", "closing_date": "2026-11-09",
                    "estimated_value_zar": 900_000}]
        r = self.s.scan(notices, today=self.today)
        self.assertEqual(r[0]["status"], "SHORTLIST")
        self.assertGreaterEqual(r[0]["score"], 0.35)

    def test_missing_certification_vetoes_match(self):
        notices = [{"reference": "T2", "title": "Civil works package", "scope": "civil works",
                    "closing_date": "2026-11-09", "estimated_value_zar": 900_000,
                    "required_certifications": ["CIDB 5CE"]}]
        r = self.s.scan(notices, today=self.today)
        self.assertEqual(r[0]["status"], "VETOED_ELIGIBILITY")

    def test_closed_tender_is_ignored(self):
        notices = [{"reference": "T3", "title": "Fire services", "scope": "fire services",
                    "closing_date": "2026-10-30", "estimated_value_zar": 100_000}]
        self.assertEqual(self.s.scan(notices, today=self.today)[0]["status"], "CLOSED")

    def test_value_outside_band_rejected(self):
        notices = [{"reference": "T4", "title": "Civil works", "scope": "civil works",
                    "closing_date": "2026-11-09", "estimated_value_zar": 99_000_000}]
        self.assertEqual(self.s.scan(notices, today=self.today)[0]["status"], "OUT_OF_VALUE_BAND")

    def test_agent_may_not_submit_tender(self):
        with self.assertRaises(PermissionDenied):
            self.s.submit_tender("T1")
        self.assertEqual(self.s.log[-1]["action_class"], "HUMAN_ONLY")

    def test_agent_may_not_sign_contract(self):
        with self.assertRaises(PermissionDenied):
            self.s.sign_contract("T1")

    def test_every_action_is_logged_with_attribution(self):
        self.s.scan([{"reference": "T5", "title": "steel supply", "scope": "reinforcement steel",
                      "closing_date": "2026-11-09", "estimated_value_zar": 500_000}], today=self.today)
        self.assertTrue(self.s.log)
        for entry in self.s.log:
            self.assertEqual(entry["agent_id"], "tender_scout")
            self.assertIn("passport_version", entry)
            self.assertIn("timestamp_utc", entry)

    def test_bid_pack_never_contains_pricing_or_submission(self):
        pack = self.s.draft_bid_pack({"reference": "T6"})
        self.assertEqual(pack["status"], "DRAFT_FOR_HUMAN_REVIEW")
        self.assertIn("tender.submit", pack["blocked_from_agent"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
