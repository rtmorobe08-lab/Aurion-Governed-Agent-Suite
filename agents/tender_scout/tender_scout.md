# Agent 08 — Tender Scout

**Hymn:** *Hymn pending lock.*
**Tier:** Scale · **Repo module:** `agents/tender_scout` · **Status:** active (simulation first)

## Purpose
Scan tender notices and portals, match opportunities against the business's capability profile and margin floor,
and assemble a bid pack **for human review**. It never submits a tender, never signs, never prices a bid.

## The governance wall
| Action | Class | Tier |
|---|---|---|
| Read notices, score a match | READ_ONLY | T0 |
| Draft the shortlist and bid-pack checklist | DRAFT_INTERNAL | T0 |
| Notify the owner of a matched, closing-soon opportunity | NOTIFY_THEN_ACT | T1 |
| Finalise a bid pack | APPROVE_THEN_ACT | T2, human approval |
| **Submit a tender** | **HUMAN_ONLY** | **T3, blocked in code** |
| Sign a contract | HUMAN_ONLY | T3, blocked |

## Match scoring
1. Keyword overlap between notice scope and the capability profile (weighted).
2. Closing date inside the action window (default 14 days) — a tender closing tomorrow is a notification, not an opportunity.
3. Estimated value inside the declared band — below the margin floor is noise, above the capacity ceiling is a trap.
4. Exclusion terms (e.g. "CIDB Grade 5 required" when the business holds Grade 2) veto the match outright.

## Data touched
Tender reference, closing date, scope summary, estimated value, eligibility conditions. No personal information.

## Why it earns its place in the suite
The other seven agents service work you already have. This one goes and finds work, which is the fastest way to
prove value to a business that is quiet this month.
