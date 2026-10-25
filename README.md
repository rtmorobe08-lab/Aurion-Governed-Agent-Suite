# Aurion-Governed-Agent-Suite

Governed, modular artificial intelligence agent infrastructure designed for secure multi-department operations, rigorous auditability, and automated compliance (aligned with POPIA and FICA standards).

---

## 🏛️ System Architecture Overview

The Aurion Agent Suite is structured into distinct operational modules and core governance layers, ensuring complete traceability, human-in-the-loop protection, and strict regulatory adherence.

### Core Governance Engine (`core/`)
* **`master_router.py`**: Central validation and routing engine verifying all inter-agent communications.
* **`agent_passport.json` & `assurance_register.json`**: Identity schemas and incident/assurance tracking standards.
* **`executive_dashboard.py`**: Operational status summarizer providing high-level telemetry.

---

## 🤖 Operational Agent Modules (`agents/`)

The suite orchestrates six specialized agent domains:

1. **Front of House (`front_of_house/`)**: Client intake, initial request parsing, and gateway triage.
2. **Connector (`connector/`)**: External API integrations, secure data transfers, and gateway communication.
3. **Bookkeeper (`bookkeeper/`)**: Financial ledger verification, transaction allocations, and audit trails.
4. **Inventory & Payroll (`inventory_payroll/`)**: Stock threshold monitoring, resource recovery tracking, and allocation metrics.
5. **Paperwork (`paperwork/`)**: Automated compliance documentation, briefing memos, and policy draft generation.
6. **Watchtower (`watchtower/`)**: Security incident detection, anomaly monitoring, and human-gate enforcement.

---

## 🚀 Automated Testing & CI/CD

* **Master Test Runner (`run_all_agent_tests.py`)**: Executes back-to-back validations across all six agent modules to confirm routing integrity.
* **GitHub Actions CI (`.github/workflows/governance_ci.yml`)**: Automatically triggers full-suite validation checks on every push and pull request to the `main` branch.

---
*Maintained by Aurion Enterprises | Secure Multi-Agent Infrastructure*
