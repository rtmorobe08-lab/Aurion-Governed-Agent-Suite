#!/usr/bin/env python3
"""
Aurion agent governance validator.
Fails closed: any violation exits non-zero so CI blocks the merge.
Stdlib only. Run from the repo root: python governance/validate_governance.py
"""
import json, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "governance", "governance_parameters.json")
errors, warnings, checks = [], [], 0

def ok(msg):
    global checks; checks += 1

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def load(path):
    with open(path) as f: return json.load(f)

# ---------- 1. parameters file ----------
try:
    params = load(P)
    ok("parameters file parses")
except Exception as e:
    print(f"FATAL: cannot read {P}: {e}"); sys.exit(2)

for key in ["parameter_set","version","effective_date","status","posture","action_classes","action_type_map","global","agents"]:
    if key not in params: err(f"parameters missing required key: {key}")
    else: ok("")

g = params["global"]
if params["posture"]["default_behaviour"] != "fail_closed":
    err("posture must be fail_closed")
if not g["disclosure"]["required_for_external_interaction"]:
    err("global disclosure must be required")
if g["kill_switch"]["max_activation_seconds"] > 3:
    err("kill switch must engage within 3 seconds")
if g["audit"]["retention_years"] < 5:
    err("audit retention must be at least 5 years")
if g["data_protection"]["proceed_without_lawful_basis"]:
    err("agents may not proceed without a lawful basis")
if g["financial"]["payments_executed_by_agents"]:
    err("agents must not execute payments")
ok("")

# ---------- 2. action map integrity ----------
valid_classes = set(params["action_classes"].keys())
for action, cls in params["action_type_map"].items():
    if cls not in valid_classes: err(f"action '{action}' maps to unknown class '{cls}'")
ok("")

# ---------- 3. per-agent passports ----------
caps = {"h": g["financial"]["per_hour_cap"], "d": g["financial"]["per_day_cap"]}
declared = params["agents"]
found_dirs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT,"agents","*","passport.json")))

for aid, a in declared.items():
    ppath = os.path.join(ROOT, "agents", aid, "passport.json")
    if not os.path.exists(ppath):
        err(f"[{aid}] passport.json missing"); continue
    try:
        pp = load(ppath); ok("")
    except Exception as e:
        err(f"[{aid}] passport is not valid JSON: {e}"); continue

    for f in ["agent_id","agent_name","passport_version","owner","purpose","status","commercial_tier",
              "data_classes","allowed_actions","prohibited_actions","runtime_governance","audit","review"]:
        if f not in pp: err(f"[{aid}] passport missing field: {f}")
    if pp.get("agent_id") != aid: err(f"[{aid}] passport agent_id does not match folder")
    if len(pp.get("purpose","")) < 20: err(f"[{aid}] purpose too thin to be auditable")
    if pp.get("status") != a["status"]: err(f"[{aid}] status mismatch parameters vs passport")
    if pp.get("commercial_tier") != a["commercial_tier"]: err(f"[{aid}] tier mismatch")

    extra_data = set(pp.get("data_classes",[])) - set(a["data_classes_allowed"])
    if extra_data: err(f"[{aid}] passport claims data classes not authorised: {sorted(extra_data)}")
    extra_actions = set(pp.get("allowed_actions",[])) - set(a["action_classes_allowed"])
    if extra_actions: err(f"[{aid}] passport claims action classes not authorised: {sorted(extra_actions)}")
    missing_prohib = set(a["prohibited_actions"]) - set(pp.get("prohibited_actions",[]))
    if missing_prohib: err(f"[{aid}] passport omits prohibited actions: {sorted(missing_prohib)}")

    rg = pp.get("runtime_governance",{})
    if rg.get("kill_switch_active") is not True: err(f"[{aid}] kill switch not active")
    if rg.get("kill_switch_max_seconds",99) > 3: err(f"[{aid}] kill switch slower than 3 seconds")
    if rg.get("disclosure_required") is not True: err(f"[{aid}] disclosure not required")
    if rg.get("zar_spend_cap_hourly",0) > caps["h"]: err(f"[{aid}] hourly cap exceeds global ceiling")
    if rg.get("zar_spend_cap_daily",0) > caps["d"]: err(f"[{aid}] daily cap exceeds global ceiling")
    if pp.get("audit",{}).get("retention_years",0) < 5: err(f"[{aid}] audit retention under 5 years")
    if pp.get("audit",{}).get("logs_appended_only") is not True: err(f"[{aid}] logs must be append-only")
    for r in ["owner_attestation","governance_audit"]:
        if not pp.get("review",{}).get(r): err(f"[{aid}] review.{r} missing")
    # canon-pending agents must not claim a module
    if pp.get("status") == "canon_pending_module" and a.get("repo_module"):
        err(f"[{aid}] declared pending but claims a repo module")
    # external-facing disclosure
    if aid in ("front_of_house",) and rg.get("disclosure_required") is not True:
        err(f"[{aid}] external-facing agent must disclose")
    # payments never agent-executed
    if "payment.initiate" in pp.get("allowed_actions",[]) or "HUMAN_ONLY" in pp.get("allowed_actions",[]):
        err(f"[{aid}] passport implies agents may initiate payments or take human-only actions")

for d in found_dirs:
    if d not in declared: warn(f"agent folder '{d}' has a passport but is not declared in governance parameters")

# ---------- 3b. agent behaviour assurance (v1.1) ----------
for key in ("permission_model","monitoring_independence","evidence_chain","adversarial_test_battery"):
    if key not in g: err(f"global parameters missing '{key}' (agent behaviour assurance)")
    else: ok("")
if g.get("monitoring_independence",{}).get("architecture") != "two_lock":
    err("monitoring must be two-lock: an independent monitor, not only an agent")
for aid in declared:
    pj = load(os.path.join(ROOT,"agents",aid,"passport.json"))
    if pj.get("permissions",{}).get("mode") != "deny_by_default":
        err(f"[{aid}] permission model is not deny-by-default")
    if pj.get("permissions",{}).get("may_modify_own_controls") is not False:
        err(f"[{aid}] agent may modify its own controls")
    if pj.get("monitoring",{}).get("independent_monitor_required") is not True:
        err(f"[{aid}] no independent monitor declared")
    if pj.get("monitoring",{}).get("divergence_action") != "suspend_and_open_incident":
        err(f"[{aid}] divergence from the independent log does not suspend the agent")
    if pj.get("evidence",{}).get("chain") != "hash_chained_out_of_band":
        err(f"[{aid}] evidence chain is not hash-chained and captured out of band")
    if pj.get("evidence",{}).get("reconciled_per_incident") is not True:
        err(f"[{aid}] agent account is not reconciled per incident")
    if pj.get("assurance",{}).get("adversarial_test_battery") != "required_before_go_live":
        err(f"[{aid}] adversarial test battery not required before go-live")
ok("")

# ---------- 4. register linkage ----------
reg_path = os.path.join(ROOT,"core","assurance_register_schema.json")
if os.path.exists(reg_path):
    reg = load(reg_path)
    if "agent_id" not in json.dumps(reg): warn("assurance register schema has no agent_id field; agent events cannot be attributed")
else:
    warn("no assurance register schema found")

# ---------- report ----------
print(f"governance validation: {checks} checks passed, {len(warnings)} warnings, {len(errors)} errors")
for w in warnings: print(f"  WARN  {w}")
for e in errors:   print(f"  FAIL  {e}")
if errors:
    print("\nRESULT: BLOCKED — the suite does not satisfy its own governance parameters.")
    sys.exit(1)
print("\nRESULT: PASS — every declared agent satisfies the governance parameters.")
