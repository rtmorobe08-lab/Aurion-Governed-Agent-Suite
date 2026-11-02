# Governance layer of the Aurion Governed Agent Suite

| File | Purpose |
|---|---|
| `governance/GOVERNANCE_CHARTER.md` | Plain-language charter for clients, auditors and funders |
| `governance/governance_parameters.json` | The normative parameter set: tiers, caps, limits, gates, retention |
| `governance/governance_parameters.schema.json` | JSON Schema for the parameters file |
| `governance/validate_governance.py` | Fail-closed validator: exits non-zero when any agent breaks its parameters |
| `agents/<agent_id>/passport.json` | The passport each agent must carry |
| `core/agent_passport_schema.json` | Schema v2 for passports |

Eight agents are declared: Front of House, Bookkeeper, Paperwork, Connector, Inventory and Supplier,
Payroll, Watchtower, Tender Scout. Two carry caveats:
- Inventory and Payroll share the `agents/inventory_payroll` module but are governed separately.
- Tender Scout is `canon_pending_module`: declared canon, no module yet. It must not be described as deployed.

## What CI must enforce from now on (handover to Gemini)
1. Run `python governance/validate_governance.py` on every push and pull request to `main`; a non-zero exit blocks the merge.
2. Keep the existing tests and module checks; add the governance step after them.
3. Fail the build if any agent folder lacks a `passport.json`, or if a passport's `status` is `canon_pending_module` while a module directory exists.
4. Print a one-line governance summary at the end of the job so the status is visible in the Actions log.
5. Do not weaken the validator to make a build pass. If a rule is wrong, change the parameter and raise a version bump.

## Ratification pending (Director)
1. Spend caps: per action R500, per hour R2,000, per day R10,000, per month R40,000.
2. Kill-switch authorised roles.
3. Named Governance Lead (currently a placeholder).
4. Retention: logs five years, call recordings ninety days.
5. Tender Scout hymn (unlocked) and whether it gets its own module this quarter.
