# Agent architecture: separate agents, shared capabilities

Decision recorded 2 November 2026. Applies to the eight canon agents.

## The question
Should several agents share one code module (as Inventory and Payroll do), or should every agent get its own?

## The decision
**Governance is per agent. Code is shared where the capability is genuinely the same.**

1. **One folder per agent** under `agents/<agent_id>/`, containing that agent's `passport.json`, its tests,
   its entrypoint, and its README. Eight agents, eight folders, no exceptions.
2. **Shared capability code lives in `core/`** — ledger access, document generation, portal clients, the master
   router. If two agents need the same capability, they import it; they do not copy it.
3. **A module may be shared; a passport may not.** Inventory and Payroll currently share
   `agents/inventory_payroll` as their code home while remaining two separately governed agents.

## Why not merge everything into fewer modules
1. **Kill-switch granularity.** A client must be able to stop Payroll without stopping Inventory. If they share
   one runtime, the kill switch becomes a blunt instrument and someone will avoid using it.
2. **Attribution.** Every register entry names one agent. A shared module blurs "which agent did this", which is
   the first question an auditor, a funder or a court asks.
3. **Packaging.** A Starter client buys Front of House only. Every agent must be independently shippable,
   independently priced and independently switched off.
4. **Different risk profiles.** Payroll touches money-adjacent data and needs T3 walls; Inventory drafts purchase
   orders under a cap. One module forces one posture on both.
5. **Different change cadence.** Payroll changes with legislation; Inventory changes with the storeroom.

## Why not duplicate everything per agent
That is the opposite failure: eight copies of ledger access means eight places to fix a bug and eight chances to
drift. Shared code in `core/` keeps one behaviour, one test, one fix. The rule of thumb: **share capability,
separate identity.**

## Consequences to honour
- A shared module must never embed agent-specific governance. Caps, gates and disclosure are read from the
  agent's passport at runtime, not hard-coded in the shared code.
- Shared code changes require re-running every agent's tests, not just the one that prompted the change.
- When Inventory and Payroll diverge materially (different data sources, different schemas), split the module.
  Until then, the shared home is recorded in both passports so nobody is surprised.

## Current mapping
| Agent | Code home | Governance |
|---|---|---|
| Front of House | `agents/front_of_house` | own passport |
| Bookkeeper | `agents/bookkeeper` | own passport |
| Paperwork | `agents/paperwork` | own passport |
| Connector | `agents/connector` | own passport |
| Inventory and Supplier | `agents/inventory_payroll` (shared) | own passport |
| Payroll | `agents/inventory_payroll` (shared) | own passport |
| Watchtower | `agents/watchtower` | own passport |
| Tender Scout | `agents/tender_scout` | own passport |
