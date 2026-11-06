#!/usr/bin/env python3
"""Governance-audit harness: Ethereum + Cosmos Hub (live primary sources).

Stdlib only. Fetches live data, saves every raw retrieval under
outputs/raw/ with timestamps, scores the 12 rubric rules (rubric.md),
and writes outputs/results.json + outputs/results.txt.

Run:  python3 src/fetch_governance.py
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "outputs", "raw")
OUT = os.path.join(BASE, "outputs")
os.makedirs(RAW, exist_ok=True)

WIB = timezone(timedelta(hours=7))
UA = {"User-Agent": "gov-audit-harness/1.0 (research; contact: public repo)"}

PECTRA_EIPS = [2537, 2935, 6110, 7002, 7251, 7549, 7623, 7642, 7685, 7691, 7702, 7840]
FUSAKA_EIPS = [7594, 7823, 7825, 7883, 7892, 7642, 7910, 7917, 7918, 7934, 7935, 7939, 7951]
DENCUN_EIPS = [1153, 4788, 4844, 5656, 6780, 7044, 7045, 7514, 7516]
SAMPLE_EIPS = [1, 1559, 2718, 2930, 4895, 3675, 4399, 20, 721, 1155, 4337]
EIP_SET = sorted(set(PECTRA_EIPS + FUSAKA_EIPS + DENCUN_EIPS + SAMPLE_EIPS))

LOG = []


def stamp():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ"), now.astimezone(WIB).strftime("%Y-%m-%d %H:%M:%S WIB")


def log(msg):
    utc, wib = stamp()
    line = f"[{wib} / {utc}] {msg}"
    print(line, flush=True)
    LOG.append(line)


def fetch(url, name, range_bytes=None):
    """GET url, save raw bytes to outputs/raw/<name>, return (ok, path, meta)."""
    headers = dict(UA)
    if range_bytes:
        headers["Range"] = f"bytes=0-{range_bytes}"
    req = urllib.request.Request(url, headers=headers)
    utc, wib = stamp()
    data, status = None, None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                status = r.status
            break
        except urllib.error.HTTPError as e:
            data = e.read()
            status = e.code
            if status == 403 and attempt == 1:
                log(f"FETCH 403 (rate limit?) {url} — waiting 65s and retrying once")
                time.sleep(65)
                continue
            break
        except Exception as e:  # network failure
            log(f"FETCH FAIL {url} :: {e}")
            return False, None, {"url": url, "status": None, "error": str(e),
                                 "retrieved_utc": utc, "retrieved_wib": wib}
    if data is None:
        log(f"FETCH FAIL {url} :: no data")
        return False, None, {"url": url, "status": status,
                             "retrieved_utc": utc, "retrieved_wib": wib}
    path = os.path.join(RAW, name)
    with open(path, "wb") as f:
        f.write(data)
    meta = {"url": url, "status": status, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "file": f"outputs/raw/{name}",
            "retrieved_utc": utc, "retrieved_wib": wib}
    log(f"FETCH {status} {len(data)}b {url} -> {name}")
    return status in (200, 206), path, meta


def front_matter(text):
    """Parse YAML-ish front matter between the first two --- lines."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main():
    results = {"rules": {}, "measurements": {}, "sources": {}}
    now_utc, now_wib = stamp()
    results["run"] = {"started_utc": now_utc, "started_wib": now_wib}
    log("harness start")

    # ---- Ethereum: EIPs git tree -------------------------------------
    ok, _, meta = fetch("https://api.github.com/repos/ethereum/EIPs/git/trees/master?recursive=1",
                        "eth_eips_tree.json")
    results["sources"]["eth_eips_tree"] = meta
    tree = {}
    if ok:
        tree = json.load(open(os.path.join(RAW, "eth_eips_tree.json")))
    eip_files = [t["path"] for t in tree.get("tree", [])
                 if t["path"].startswith("EIPS/eip-") and t["path"].endswith(".md")]
    results["measurements"]["eip_file_count"] = len(eip_files)
    results["measurements"]["eip_tree_truncated"] = tree.get("truncated")
    results["measurements"]["eip_tree_sha"] = tree.get("sha")
    log(f"EIP files in tree: {len(eip_files)} (truncated={tree.get('truncated')})")

    # ---- Ethereum: EIP front matter (Range fetch, first 2 KiB) --------
    fm_status = {}
    fm_meta = {}
    for n in EIP_SET:
        ok, _, m = fetch(
            f"https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-{n}.md",
            f"eth_eip_{n}.md", range_bytes=2047)
        fm_meta[n] = m
        if ok:
            txt = open(os.path.join(RAW, f"eth_eip_{n}.md"), errors="replace").read()
            fm = front_matter(txt)
            fm_status[n] = fm.get("status") if fm else None
            if fm is None:
                log(f"EIP-{n}: front matter NOT parseable")
        else:
            fm_status[n] = None
        time.sleep(0.2)
    results["sources"]["eth_eip_frontmatter"] = fm_meta
    results["measurements"]["eip_frontmatter_status"] = {str(k): v for k, v in fm_status.items()}
    log(f"EIP front matter fetched for {len(EIP_SET)} EIPs")

    # ---- Ethereum: all-forks.json ------------------------------------
    ok, _, meta = fetch("https://raw.githubusercontent.com/ethereum/pm/master/all-forks.json",
                        "eth_all_forks.json")
    results["sources"]["eth_all_forks"] = meta
    forks = {}
    if ok:
        forks = json.load(open(os.path.join(RAW, "eth_all_forks.json")))
    results["measurements"]["all_forks_schema_version"] = forks.get("schema_version")
    fork_list = forks.get("forks", [])
    by_name = {}
    for f in fork_list:
        nm = f.get("combined_name") or (f.get("name", {}).get("execution") or "")
        by_name[nm] = f
    results["measurements"]["fork_count"] = len(fork_list)
    results["measurements"]["pectra_eips"] = by_name.get("Pectra", {}).get("eips")
    results["measurements"]["fusaka_eips"] = by_name.get("Fusaka", {}).get("eips")
    results["measurements"]["fusaka_activation"] = by_name.get("Fusaka", {}).get("activation")
    active = [f for f in fork_list if f.get("status") == "active"]
    latest_active = max(active, key=lambda f: (f.get("activation", {}).get("timestamp") or 0))
    la_name = latest_active.get("combined_name") or latest_active.get("name", {}).get("execution")
    results["measurements"]["latest_active_fork"] = {
        "name": la_name, "status": latest_active.get("status"),
        "activation": latest_active.get("activation")}
    planned = [f.get("combined_name") or f.get("name", {}).get("execution")
               for f in fork_list if f.get("status") == "planned"]
    results["measurements"]["planned_forks"] = planned
    log(f"forks: {len(fork_list)}; latest active: {la_name} "
        f"@{latest_active.get('activation', {}).get('timestamp')}; planned: {planned}")

    # ---- Ethereum: pm README meeting table ---------------------------
    ok, _, meta = fetch("https://raw.githubusercontent.com/ethereum/pm/master/README.md",
                        "eth_pm_readme.md")
    results["sources"]["eth_pm_readme"] = meta
    acd_rows = []
    if ok:
        txt = open(os.path.join(RAW, "eth_pm_readme.md"), errors="replace").read()
        # rows: | 29 Oct 2026 | ACDC | 190 | ...
        for m in re.finditer(r"\|\s*(\d{1,2} [A-Z][a-z]{2} \d{4})\s*\|\s*(ACDE|ACDC|ACDT)\s*\|\s*(\d+)\s*\|", txt):
            d = datetime.strptime(m.group(1), "%d %b %Y").replace(tzinfo=timezone.utc)
            acd_rows.append({"date": m.group(1), "type": m.group(2),
                             "number": int(m.group(3)), "epoch_days_ago":
                             (datetime.now(timezone.utc) - d).days})
    results["measurements"]["acd_table_rows"] = len(acd_rows)
    latest = {}
    for t in ("ACDE", "ACDC"):
        rows = [r for r in acd_rows if r["type"] == t]
        if rows:
            latest[t] = rows[0]
    results["measurements"]["acd_latest"] = latest
    log(f"ACD table rows: {len(acd_rows)}; latest ACDE={latest.get('ACDE')}; latest ACDC={latest.get('ACDC')}")

    # ---- Ethereum: ACD meeting-note directories (staleness check) -----
    ok_el, _, meta_el = fetch(
        "https://api.github.com/repos/ethereum/pm/contents/AllCoreDevs-EL-Meetings",
        "eth_acd_el_dir.json")
    ok_cl, _, meta_cl = fetch(
        "https://api.github.com/repos/ethereum/pm/contents/AllCoreDevs-CL-Meetings",
        "eth_acd_cl_dir.json")
    results["sources"]["eth_acd_el_dir"] = meta_el
    results["sources"]["eth_acd_cl_dir"] = meta_cl
    dir_notes = {}
    for label, okx, fname in (("el", ok_el, "eth_acd_el_dir.json"),
                              ("cl", ok_cl, "eth_acd_cl_dir.json")):
        if okx:
            items = json.load(open(os.path.join(RAW, fname)))
            names = [i["name"] for i in items]
            nums = []
            for n in names:
                m = re.search(r"(\d+)", n)
                if m and ("eeting" in n.lower() or n.lower().startswith("call_")):
                    nums.append(int(m.group(1)))
            dir_notes[label] = {"count": len(names), "max_number": max(nums) if nums else None}
    results["measurements"]["acd_note_dirs"] = dir_notes
    log(f"ACD note dirs: {dir_notes}")

    # latest EL meeting note date + latest CL call note date (Range fetch)
    for label, fname in (("el", "Meeting 204.md"), ("cl", "call_150.md")):
        folder = "AllCoreDevs-EL-Meetings" if label == "el" else "AllCoreDevs-CL-Meetings"
        ok, _, m = fetch(
            f"https://raw.githubusercontent.com/ethereum/pm/master/{folder}/{urllib.request.quote(fname)}",
            f"eth_acd_{label}_latest.md", range_bytes=2047)
        results["sources"][f"eth_acd_{label}_latest"] = m
        if ok:
            txt = open(os.path.join(RAW, f"eth_acd_{label}_latest.md"), errors="replace").read()
            dm = re.search(r"Meeting Date/Time:\s*([^\n<]+)", txt)
            results["measurements"][f"acd_{label}_latest_note_date"] = dm.group(1).strip() if dm else None
    log(f"latest note dates: EL={results['measurements'].get('acd_el_latest_note_date')}; "
        f"CL={results['measurements'].get('acd_cl_latest_note_date')}")

    # ---- Ethereum: client diversity ----------------------------------
    # The page carries several datasets per layer in separate divs; parse
    # each one separately (label regex allows whole or decimal percents).
    # Visible defaults: execution = "supermajority" (validator-weighted),
    # consensus = "migalabs". Hidden: execution "ethernodes" (node share);
    # consensus "blockprint" and "rated".
    ok, _, meta = fetch("https://clientdiversity.org/", "eth_client_diversity.html")
    results["sources"]["eth_client_diversity"] = meta
    datasets = {"execution": {}, "consensus": {}}
    if ok:
        html = open(os.path.join(RAW, "eth_client_diversity.html"), errors="replace").read()

        def parse_dataset(seg):
            out = {}
            for m in re.finditer(
                    r'<label class="form-label[^>]*>\s*([A-Za-z][A-Za-z ]*?)\s*-\s*(\d+(?:\.\d+)?)%\s*</label>', seg):
                out[m.group(1).strip()] = float(m.group(2))
            return out

        def dataset_div(html, layer_marker, dataset):
            # Slice the layer section into per-dataset divs: a dataset's
            # segment runs from its own div start to the NEXT dataset div
            # start (any dataset), so values from a later dataset cannot
            # overwrite an earlier one.
            i = html.find(layer_marker)
            seg = html[i:i + 90000] if i >= 0 else ""
            pat = re.compile(r'<div class="([^"]*\b(blockprint|migalabs|rated|ethernodes|supermajority)\b[^"]*)">')
            starts = [(m.start(), m.group(2)) for m in pat.finditer(seg)]
            for idx, (s, name) in enumerate(starts):
                if name == dataset:
                    e = starts[idx + 1][0] if idx + 1 < len(starts) else len(seg)
                    return parse_dataset(seg[s:e])
            return {}

        datasets["execution"]["ethernodes"] = dataset_div(html, "Execution Clients", "ethernodes")
        datasets["execution"]["supermajority"] = dataset_div(html, "Execution Clients", "supermajority")
        datasets["consensus"]["blockprint"] = dataset_div(html, "Consensus Clients", "blockprint")
        datasets["consensus"]["migalabs"] = dataset_div(html, "Consensus Clients", "migalabs")
        datasets["consensus"]["rated"] = dataset_div(html, "Consensus Clients", "rated")
        # staleness warning text on the visible execution dataset
        sw = re.search(r"Data is stale.*?(This data set is mostly comprised[^<]+)", html, re.S)
        datasets["execution_supermajority_stale_note"] = (
            sw.group(1).strip() if sw else None)
        # consensus supermajority alert text (visible alert)
        al = re.search(r"Teku has a supermajority[^<]*", html)
        datasets["consensus_alert_text"] = al.group(0).strip() if al else None
    results["measurements"]["client_diversity_datasets"] = datasets
    exec_shares = datasets["execution"].get("ethernodes", {})
    cons_shares = datasets["consensus"].get("migalabs", {})
    log(f"execution datasets: {datasets['execution']}")
    log(f"consensus datasets: {datasets['consensus']}")
    log(f"stale note: {datasets.get('execution_supermajority_stale_note')}")

    # ---- Ethereum: /all page row count --------------------------------
    ok, _, meta = fetch("https://eips.ethereum.org/all", "eth_eips_all.html")
    results["sources"]["eth_eips_all"] = meta
    if ok:
        html = open(os.path.join(RAW, "eth_eips_all.html"), errors="replace").read()
        rows = len(re.findall(r'<td class="eipnum"><a href="/EIPS/eip-\d+">', html))
        results["measurements"]["eips_all_page_rows"] = rows
        page_nums = set(int(n) for n in re.findall(
            r'<td class="eipnum"><a href="/EIPS/eip-(\d+)">', html))
        tree_nums = set(int(re.search(r"eip-(\d+)\.md", p).group(1)) for p in eip_files)
        missing = sorted(page_nums - tree_nums)
        results["measurements"]["eips_page_not_in_tree"] = missing
        results["measurements"]["eips_page_not_in_tree_count"] = len(missing)
        log(f"/all page EIP rows: {rows}; numbers on page but not in tree: {len(missing)}")
        # Verify the split hypothesis on samples: ERCs should exist in the
        # ethereum/ERCs repo (ERCs were split out of EIPs in 2025).
        if missing:
            samples = sorted({missing[0], 7524, missing[-1]} & set(missing))
            checks = {}
            for sample in samples:
                ok2, _, m2 = fetch(
                    f"https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-{sample}.md",
                    f"eth_erc_{sample}_head.md", range_bytes=2047)
                results["sources"][f"eth_erc_{sample}"] = m2
                checks[sample] = bool(ok2)
                time.sleep(0.2)
            results["measurements"]["erc_split_samples"] = checks
            log(f"ERC-split samples in ethereum/ERCs: {checks}")

    # ---- Cosmos: proposals -------------------------------------------
    ok, _, meta = fetch(
        "https://lcd-cosmoshub.keplr.app/cosmos/gov/v1/proposals?pagination.limit=50&pagination.reverse=true",
        "cosmos_proposals.json")
    results["sources"]["cosmos_proposals"] = meta
    props = []
    if ok:
        props = json.load(open(os.path.join(RAW, "cosmos_proposals.json"))).get("proposals", [])
    results["measurements"]["cosmos_proposals_returned"] = len(props)
    results["measurements"]["cosmos_latest_proposal"] = (
        {"id": props[0].get("id"), "status": props[0].get("status"),
         "title": props[0].get("title")} if props else None)
    decided = [p for p in props if p.get("status") in
               ("PROPOSAL_STATUS_PASSED", "PROPOSAL_STATUS_REJECTED")]
    results["measurements"]["cosmos_decided_count_in_50"] = len(decided)
    log(f"Cosmos proposals: {len(props)} returned; latest id={props[0].get('id') if props else None}; "
        f"decided in window: {len(decided)}")

    # ---- Cosmos: params ----------------------------------------------
    ok, _, meta = fetch("https://lcd-cosmoshub.keplr.app/cosmos/gov/v1/params/voting",
                        "cosmos_params_voting.json")
    results["sources"]["cosmos_params_voting"] = meta
    voting = {}
    if ok:
        voting = json.load(open(os.path.join(RAW, "cosmos_params_voting.json"))).get("params", {})
    results["measurements"]["cosmos_voting_params"] = voting
    ok, _, meta = fetch("https://lcd-cosmoshub.keplr.app/cosmos/gov/v1/params/deposit",
                        "cosmos_params_deposit.json")
    results["sources"]["cosmos_params_deposit"] = meta
    deposit = {}
    if ok:
        deposit = json.load(open(os.path.join(RAW, "cosmos_params_deposit.json"))).get("params", {})
    results["measurements"]["cosmos_deposit_params"] = deposit
    log(f"Cosmos voting params: {voting}")
    log(f"Cosmos deposit params: {deposit}")

    # ---- Cosmos: staking pool + validators ---------------------------
    ok, _, meta = fetch("https://lcd-cosmoshub.keplr.app/cosmos/staking/v1beta1/pool",
                        "cosmos_pool.json")
    results["sources"]["cosmos_pool"] = meta
    pool = {}
    if ok:
        pool = json.load(open(os.path.join(RAW, "cosmos_pool.json"))).get("pool", {})
    bonded = int(pool.get("bonded_tokens", "0") or 0)
    results["measurements"]["cosmos_bonded_tokens_uatom"] = bonded
    ok, _, meta = fetch(
        "https://lcd-cosmoshub.keplr.app/cosmos/staking/v1beta1/validators?pagination.limit=200&status=BOND_STATUS_BONDED",
        "cosmos_validators.json")
    results["sources"]["cosmos_validators"] = meta
    validators = []
    if ok:
        validators = json.load(open(os.path.join(RAW, "cosmos_validators.json"))).get("validators", [])
    results["measurements"]["cosmos_bonded_validators"] = len(validators)
    top10 = 0
    if validators and bonded:
        toks = sorted((int(v.get("tokens", "0") or 0) for v in validators), reverse=True)
        top10 = sum(toks[:10])
        results["measurements"]["cosmos_top10_tokens_uatom"] = top10
        results["measurements"]["cosmos_top10_share"] = round(top10 / bonded, 4)
        results["measurements"]["cosmos_top1_share"] = round(toks[0] / bonded, 4)
    log(f"Cosmos bonded: {bonded} uatom; validators: {len(validators)}; top10 share: "
        f"{results['measurements'].get('cosmos_top10_share')}")

    # ---- Cosmos: tallies for last 5 decided proposals ----------------
    turnouts = []
    for p in decided[:5]:
        pid = p["id"]
        ok, _, m = fetch(f"https://lcd-cosmoshub.keplr.app/cosmos/gov/v1/proposals/{pid}/tally",
                         f"cosmos_tally_{pid}.json")
        results["sources"][f"cosmos_tally_{pid}"] = m
        if ok and bonded:
            t = json.load(open(os.path.join(RAW, f"cosmos_tally_{pid}.json"))).get("tally", {})
            total = sum(int(t.get(k, "0") or 0) for k in
                        ("yes_count", "abstain_count", "no_count", "no_with_veto_count"))
            turnouts.append({"id": pid, "status": p["status"],
                             "turnout": round(total / bonded, 4),
                             "yes": t.get("yes_count"), "no": t.get("no_count"),
                             "abstain": t.get("abstain_count"),
                             "no_with_veto": t.get("no_with_veto_count")})
        time.sleep(0.2)
    results["measurements"]["cosmos_last5_turnouts"] = turnouts
    log(f"turnouts: {turnouts}")

    # ---- Cosmos: voting windows for last 10 decided ------------------
    # Standard proposals: 604800s. Expedited proposals (flagged expedited):
    # 259200s. Both are correct; anything else is a deviation.
    windows = []
    for p in decided[:10]:
        vs, ve = p.get("voting_start_time"), p.get("voting_end_time")
        secs = None
        if vs and ve:
            try:
                t0 = datetime.fromisoformat(vs.replace("Z", "+00:00"))
                t1 = datetime.fromisoformat(ve.replace("Z", "+00:00"))
                secs = int((t1 - t0).total_seconds())
            except ValueError:
                secs = None
        expected = 259200 if p.get("expedited") else 604800
        windows.append({"id": p["id"], "expedited": bool(p.get("expedited")),
                        "voting_window_seconds": secs, "expected_seconds": expected,
                        "matches_expected": secs == expected})
    results["measurements"]["cosmos_last10_voting_windows"] = windows
    log(f"voting windows: {windows}")

    # ---- Scoring ------------------------------------------------------
    R = results["rules"]

    def rule(key, result, detail):
        R[key] = {"result": result, "detail": detail}

    # ETH-1
    unparsed = [n for n in EIP_SET if fm_status.get(n) is None]
    eip1 = fm_status.get(1)
    rule("ETH-1", "PASS" if (eip1 == "Living" and not unparsed) else "FAIL",
         f"EIP-1 status={eip1}; sampled {len(EIP_SET)} EIPs, unparseable={unparsed}")
    # ETH-2
    all_upgrade = sorted(set(PECTRA_EIPS + FUSAKA_EIPS))
    non_final = {n: fm_status.get(n) for n in all_upgrade if fm_status.get(n) != "Final"}
    rule("ETH-2", "PASS" if not non_final else "FAIL",
         f"Pectra+Fusaka EIPs checked: {len(all_upgrade)}; non-Final: {non_final or 'none'}")
    # ETH-3
    acde = latest.get("ACDE", {})
    acdc = latest.get("ACDC", {})
    rule("ETH-3", "PASS" if (acde.get("epoch_days_ago", 999) <= 30 and
                             acdc.get("epoch_days_ago", 999) <= 30) else "FAIL",
         f"latest ACDE #{acde.get('number')} {acde.get('date')} ({acde.get('epoch_days_ago')}d ago); "
         f"latest ACDC #{acdc.get('number')} {acdc.get('date')} ({acdc.get('epoch_days_ago')}d ago)")
    # ETH-4
    ds = datasets
    eth_nodes = ds["execution"].get("ethernodes", {})
    super_maj = ds["execution"].get("supermajority", {})
    miga = ds["consensus"].get("migalabs", {})
    if eth_nodes and super_maj and miga:
        worst_exec = max(max(eth_nodes.values()), max(super_maj.values()))
        cons_leader = max(miga.items(), key=lambda kv: kv[1])
        rule("ETH-4", "PASS" if worst_exec < 66.6 else "FAIL",
             f"execution max across datasets: ethernodes leader "
             f"{max(eth_nodes.items(), key=lambda kv: kv[1])}, supermajority leader "
             f"{max(super_maj.items(), key=lambda kv: kv[1])} (worst {worst_exec}%); "
             f"consensus (MigaLabs, visible) leader {cons_leader}; "
             f"blockprint leader={max(ds['consensus'].get('blockprint', {'?': 0}).items(), key=lambda kv: kv[1]) if ds['consensus'].get('blockprint') else None}; "
             f"rated leader={max(ds['consensus'].get('rated', {'?': 0}).items(), key=lambda kv: kv[1]) if ds['consensus'].get('rated') else None}")
    else:
        rule("ETH-4", "UNAVAILABLE",
             f"datasets incomplete: ethernodes={bool(eth_nodes)}, supermajority={bool(super_maj)}, migalabs={bool(miga)}")
    # ETH-5
    la_ts = latest_active.get("activation", {}).get("timestamp")
    now_ts = int(datetime.now(timezone.utc).timestamp())
    planned_clean = all((by_name.get(p, {}).get("activation", {}).get("timestamp") is None)
                        for p in planned)
    rule("ETH-5", "PASS" if (la_ts and la_ts <= now_ts and planned_clean) else "FAIL",
         f"latest active fork {la_name} activated ts={la_ts} (now {now_ts}); "
         f"planned forks without activation: {planned_clean} ({planned})")
    # ETH-6
    rows = results["measurements"].get("eips_all_page_rows", 0)
    rule("ETH-6", "PASS" if (len(eip_files) >= 900 and rows >= 900) else "FAIL",
         f"git tree EIP files={len(eip_files)}; /all page rows={rows}")
    # COS-1
    rule("COS-1", "PASS" if (props and int(props[0]["id"]) >= 1000 and
                             all(p.get("id") and p.get("status") and p.get("title") for p in props))
         else "FAIL",
         f"returned={len(props)}; latest id={props[0].get('id') if props else None}; "
         f"all carry id/status/title={all(p.get('id') and p.get('status') and p.get('title') for p in props) if props else False}")
    # COS-2
    q = voting.get("quorum"); th = voting.get("threshold"); vt = voting.get("veto_threshold")
    vp = voting.get("voting_period")
    rule("COS-2", "PASS" if (q == "0.400000000000000000" and th == "0.500000000000000000"
                             and vt and vt.startswith("0.334") and vp == "604800s") else "FAIL",
         f"quorum={q}; threshold={th}; veto_threshold={vt}; voting_period={vp}")
    # COS-3
    quorum = 0.4
    bad = [t for t in turnouts if t["turnout"] < quorum]
    rule("COS-3", "PASS" if (len(turnouts) == 5 and not bad) else ("FAIL" if turnouts else "UNAVAILABLE"),
         f"last-5 turnouts: {[(t['id'], t['turnout']) for t in turnouts]}; quorum={quorum}; below-quorum={bad or 'none'}")
    # COS-4
    md = deposit.get("min_deposit", [])
    md_ok = any(d.get("denom") == "uatom" and d.get("amount") == "500000000" for d in md)
    rule("COS-4", "PASS" if (md_ok and deposit.get("max_deposit_period") == "1209600s") else "FAIL",
         f"min_deposit={md}; max_deposit_period={deposit.get('max_deposit_period')}")
    # COS-5
    top10_share = results["measurements"].get("cosmos_top10_share")
    rule("COS-5", "PASS" if (top10_share is not None and top10_share < 0.5) else ("FAIL" if top10_share is not None else "UNAVAILABLE"),
         f"top-10 validators share of bonded tokens: {top10_share} "
         f"({top10} / {bonded} uatom); validators={len(validators)}")
    # COS-6
    bad_w = [w for w in windows if not w["matches_expected"]]
    rule("COS-6", "PASS" if (len(windows) == 10 and not bad_w) else ("FAIL" if windows else "UNAVAILABLE"),
         f"last-10 voting windows: {[(w['id'], w['voting_window_seconds'], 'expedited' if w['expedited'] else 'standard') for w in windows]}; mismatches={bad_w or 'none'}")

    scored = [r for r in R.values() if r["result"] != "UNAVAILABLE"]
    passed = sum(1 for r in scored if r["result"] == "PASS")
    results["score"] = {"passed": passed, "scored": len(scored),
                        "total_rules": len(R), "points": passed * 2,
                        "max_points": len(scored) * 2}
    log(f"SCORE: {passed}/{len(scored)} rules PASS ({passed * 2}/{len(scored) * 2} points); "
        f"UNAVAILABLE: {len(R) - len(scored)}")
    for k, v in R.items():
        log(f"  {k}: {v['result']} — {v['detail'][:160]}")

    results["run"]["finished_utc"], results["run"]["finished_wib"] = stamp()
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(OUT, "results.txt"), "w") as f:
        f.write("\n".join(LOG) + "\n")
    log("wrote outputs/results.json + outputs/results.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
