"""
Tender Scout — governed scanning and shortlisting.

Governance posture (see governance/governance_parameters.json):
  * read and draft only; submission and signature are HUMAN_ONLY and blocked in code
  * no spend, no payments, no personal information
  * every action writes an attributable log record
"""
from datetime import date, datetime


class PermissionDenied(Exception):
    """Raised when an action crosses a human-only boundary."""


class TenderScout:
    AGENT_ID = "tender_scout"
    PASSPORT_VERSION = "1.0"
    PROHIBITED = ("tender.submit", "contract.sign", "payment.initiate")

    def __init__(self, capability_keywords, value_floor_zar=0, value_ceiling_zar=10_000_000,
                 window_days=14, held_certifications=None, log=None):
        self.keywords = [k.lower() for k in capability_keywords]
        self.value_floor = value_floor_zar
        self.value_ceiling = value_ceiling_zar
        self.window_days = window_days
        self.certs = [c.upper() for c in (held_certifications or [])]
        self.log = log if log is not None else []

    # ---------- governance ----------
    def _record(self, action_type, action_class, target, basis, outcome):
        self.log.append({
            "agent_id": self.AGENT_ID,
            "passport_version": self.PASSPORT_VERSION,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "action_type": action_type,
            "action_class": action_class,
            "target": target,
            "data_classes_touched": ["tender_reference", "closing_date", "scope_summary", "estimated_value"],
            "decision_basis": basis,
            "human_approver_id": None,
            "outcome": outcome,
            "reversible": True,
        })

    def submit_tender(self, tender_ref):  # pragma: no cover - guard
        self._record("tender.submit", "HUMAN_ONLY", tender_ref, "attempted by agent", "blocked")
        raise PermissionDenied(
            "tender.submit is HUMAN_ONLY. Tender Scout assembles bid packs; a human submits them."
        )

    def sign_contract(self, tender_ref):  # pragma: no cover - guard
        self._record("contract.sign", "HUMAN_ONLY", tender_ref, "attempted by agent", "blocked")
        raise PermissionDenied("contract.sign is HUMAN_ONLY. An agent may never sign.")

    # ---------- scanning ----------
    def _keyword_score(self, notice):
        scope = (notice.get("title", "") + " " + notice.get("scope", "")).lower()
        hits = [k for k in self.keywords if k in scope]
        if not hits:
            return 0.0
        return min(1.0, len(hits) / max(3, len(self.keywords)) * 1.5)

    def _cert_veto(self, notice):
        required = [c.upper() for c in notice.get("required_certifications", [])]
        missing = [c for c in required if c not in self.certs]
        return missing

    def scan(self, notices, today=None):
        today = today or date.today()
        results = []
        for n in notices:
            ref = n.get("reference", "UNKNOWN")
            missing = self._cert_veto(n)
            if missing:
                results.append({"reference": ref, "status": "VETOED_ELIGIBILITY",
                                "reason": f"missing certification: {', '.join(missing)}", "score": 0.0})
                self._record("record.read", "READ_ONLY", ref, "eligibility check", "vetoed")
                continue

            try:
                closing = date.fromisoformat(n["closing_date"])
            except Exception:
                results.append({"reference": ref, "status": "REJECTED", "reason": "unparseable closing date", "score": 0.0})
                continue

            days_left = (closing - today).days
            if days_left < 1:
                results.append({"reference": ref, "status": "CLOSED", "reason": "closing date passed", "score": 0.0})
                continue
            if days_left > self.window_days:
                results.append({"reference": ref, "status": "OUT_OF_WINDOW",
                                "reason": f"closes in {days_left} days", "score": 0.0})
                continue

            value = n.get("estimated_value_zar", 0) or 0
            if value and (value < self.value_floor or value > self.value_ceiling):
                results.append({"reference": ref, "status": "OUT_OF_VALUE_BAND",
                                "reason": f"R{value:,.0f} outside R{self.value_floor:,.0f}-R{self.value_ceiling:,.0f}",
                                "score": 0.0})
                continue

            kw = self._keyword_score(n)
            urgency = 1.0 - (days_left / max(1, self.window_days))
            score = round(0.75 * kw + 0.25 * urgency, 3)
            status = "SHORTLIST" if score >= 0.35 else "WATCH"
            results.append({"reference": ref, "status": status, "score": score,
                            "days_to_close": days_left, "title": n.get("title", "")[:70]})
            self._record("record.read", "READ_ONLY", ref, f"keyword score {kw:.2f}", status)

        results.sort(key=lambda r: r["score"], reverse=True)
        return results

    # ---------- bid pack ----------
    def draft_bid_pack(self, notice):
        ref = notice.get("reference", "UNKNOWN")
        pack = {
            "tender_reference": ref,
            "status": "DRAFT_FOR_HUMAN_REVIEW",
            "checklist": [
                "Company registration and CIPC disclosure",
                "Tax compliance status PIN and CSD registration",
                "B-BBEE certificate",
                "Method statement and programme",
                "Pricing schedule prepared by a human",
                "Eligibility certificates declared in the notice",
                "Returnable schedules signed",
            ],
            "blocked_from_agent": ["pricing.finalise", "tender.submit", "contract.sign"],
            "note": "Pricing and submission are human acts. Tender Scout assembles, a person commits.",
        }
        self._record("document.draft", "DRAFT_INTERNAL", ref, "bid pack assembled", "drafted")
        return pack


def demo():
    import json
    scout = TenderScout(
        capability_keywords=["civil works", "reinforcement steel", "water treatment", "fire services",
                             "construction", "supply and delivery"],
        value_floor_zar=50_000, value_ceiling_zar=8_000_000, window_days=14,
        held_certifications=["CIDB 2CE", "CIDB 3CE"],
    )
    notices = [
        {"reference": "RS-WTW-2026-14", "title": "Supply and fixing of reinforcement steel, Rietspruit WWTW",
         "scope": "Reinforcement steel supply and fixing, civil works on water treatment plant",
         "closing_date": "2026-11-10", "estimated_value_zar": 3_400_000},
        {"reference": "VUT-PURCO-2026-03", "title": "Campus civils package",
         "scope": "Civil works and construction of walkways", "closing_date": "2026-11-06",
         "estimated_value_zar": 1_200_000, "required_certifications": ["CIDB 5CE"]},
        {"reference": "EMF-FIRE-2026-21", "title": "Fire services maintenance",
         "scope": "Fire services hose reels and extinguisher maintenance", "closing_date": "2026-11-03",
         "estimated_value_zar": 180_000},
        {"reference": "OLD-2026-01", "title": "Steel supply", "scope": "reinforcement steel",
         "closing_date": "2026-10-20", "estimated_value_zar": 900_000},
    ]
    results = scout.scan(notices, today=date(2026, 11, 2))
    print(json.dumps({"scan": results,
                      "bid_pack": scout.draft_bid_pack(notices[0]),
                      "audit_trail_count": len(scout.log)}, indent=2))


if __name__ == "__main__":
    demo()
