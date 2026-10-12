"""GGL-1.0 Section E lineage: hash-linked tree of inventors and enrichments.

  ggl.py lineage init      PARAMS.ggl.md -o LINEAGE.json [--material FILE]
  ggl.py lineage add       LINEAGE.json --name N --orcid O --parents H[,H] ... (see --help)
  ggl.py lineage recognize LINEAGE.json --node H --parent H --by-orcid O --doi D
  ggl.py lineage verify    LINEAGE.json [--license PARAMS.ggl.md] [--pool-cap PCT]
  ggl.py lineage path      LINEAGE.json NODE

Hashes are SHA-256 over canonical JSON (sorted keys, no whitespace, UTF-8), which equals
RFC 8785 for these records because they hold only strings, integers, booleans, and null.
"""
import argparse, datetime, hashlib, json, re, sys

TERMS = ("contributed", "inherit", "reserved")

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def rec_hash(rec):
    return hashlib.sha256(canon({k: v for k, v in rec.items() if k != "hash"})).hexdigest()

def sha_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def today():
    return datetime.date.today().isoformat()

def load(path):
    return json.load(open(path, encoding="utf-8"))

def save(path, data):
    open(path, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def find(data, ref):
    hits = [n for n in data["nodes"] if n["hash"].startswith(ref)]
    if len(hits) != 1:
        sys.exit(f"node '{ref}': {'not found' if not hits else 'ambiguous'}")
    return hits[0]

def doi_ok(v):
    return bool(v) and bool(re.fullmatch(r"10\.\d{4,9}/\S+", v)) and "XXXX" not in v

def cmd_init(a, g):
    vals = g.parse_header(open(a.params, encoding="utf-8").read())
    for k in ("INVENTOR_NAME", "INVENTOR_ORCID", "INVENTOR_RECORD_DOI", "COVERED_WORK", "COVERED_WORK_VERSION"):
        err = g.check_value(dict((x[1], x[2]) for x in g.load_spec())[k], vals.get(k, ""))
        if err:
            sys.exit(f"{k}: {err}. The root node needs it.")
    root = {
        "kind": "root", "parents": [],
        "contributor": {"name": vals["INVENTOR_NAME"], "orcid": vals["INVENTOR_ORCID"]},
        "builds_on": {"work": vals["COVERED_WORK"], "version": vals["COVERED_WORK_VERSION"]},
        "scope": {"sections": ["all"], "claims": ["all"], "description": "Original invention and specification"},
        "material_sha256": sha_file(a.material) if a.material else None,
        "terms": "root", "reserved_price_url": None, "pool_share_pct": "0",
        "require_enrichment_line": False, "root_claims_touched": False, "assignment_ref": None,
        "record_doi": vals["INVENTOR_RECORD_DOI"], "created": a.date or today(),
    }
    root["hash"] = rec_hash(root)
    save(a.out, {"ggl": "1.0", "covered_work": vals["COVERED_WORK"], "nodes": [root], "recognitions": []})
    print(f"root {root['hash']}")

def cmd_add(a, g):
    data = load(a.lineage)
    parents = [find(data, p)["hash"] for p in a.parents.split(",")]
    if a.terms not in TERMS:
        sys.exit("--terms must be contributed, inherit, or reserved")
    node = {
        "kind": "enrichment", "parents": parents,
        "contributor": {"name": a.name, "orcid": a.orcid},
        "builds_on": {"work": a.work or data["covered_work"], "version": a.version},
        "scope": {"sections": [s for s in (a.sections or "").split(",") if s],
                  "claims": [c for c in (a.claims or "").split(",") if c], "description": a.description},
        "material_sha256": sha_file(a.material) if a.material else a.material_sha,
        "terms": a.terms, "reserved_price_url": a.price_url,
        "pool_share_pct": "0" if a.terms == "reserved" else (a.pool_share or "0"),
        "require_enrichment_line": a.enrichment_line, "root_claims_touched": a.touches_root_claims,
        "assignment_ref": a.assignment, "record_doi": a.doi, "created": a.date or today(),
    }
    node["hash"] = rec_hash(node)
    data["nodes"].append(node)
    save(a.lineage, data)
    print(f"node {node['hash']}")

def cmd_recognize(a, g):
    data = load(a.lineage)
    node, parent = find(data, a.node), find(data, a.parent)
    rec = {"node": node["hash"], "parent": parent["hash"], "by_orcid": a.by_orcid,
           "record_doi": a.doi, "date": a.date or today(),
           "statement": "I recognize this node as an enrichment of my node under GGL-1.0 Section E."}
    rec["hash"] = rec_hash(rec)
    data["recognitions"].append(rec)
    save(a.lineage, data)
    print(f"recognition {rec['hash']}")

def analyze(data, g, pool_cap):
    errs, warn = [], []
    nodes = data["nodes"]
    by = {}
    for i, n in enumerate(nodes):
        tag = n.get("hash", "?")[:12]
        if rec_hash(n) != n.get("hash"):
            errs.append(f"{tag}: hash does not match its contents (altered)")
        for p in n["parents"]:
            if p not in by:
                errs.append(f"{tag}: parent {p[:12]} missing or listed after the child")
        if not g.orcid_ok(n["contributor"]["orcid"]):
            errs.append(f"{tag}: contributor ORCID invalid")
        by[n["hash"]] = n
        if i == 0:
            if n["kind"] != "root" or n["parents"]:
                errs.append(f"{tag}: first node must be the root, with no parents")
            continue
        if n["kind"] != "enrichment" or not n["parents"]:
            errs.append(f"{tag}: only one root is allowed; enrichments need at least one parent")
        if n["terms"] not in TERMS:
            errs.append(f"{tag}: terms must be contributed, inherit, or reserved")
        if n["terms"] == "reserved" and not (n["reserved_price_url"] or "").startswith("https://"):
            errs.append(f"{tag}: Reserved needs an https price URL (E.5)")
        if n["terms"] == "reserved" and n["pool_share_pct"] != "0":
            errs.append(f"{tag}: Reserved nodes take no pool share (E.7)")
        if not re.fullmatch(r"\d+(\.\d+)?", n["pool_share_pct"]):
            errs.append(f"{tag}: pool_share_pct must be a number")
        if not n["material_sha256"] or not re.fullmatch(r"[0-9a-f]{64}", n["material_sha256"]):
            warn.append(f"{tag}: no material hash; the contribution itself is not pinned")
    recs = {}
    for r in data["recognitions"]:
        if rec_hash(r) != r.get("hash"):
            errs.append(f"recognition {r.get('hash','?')[:12]}: altered")
            continue
        n, p = by.get(r["node"]), by.get(r["parent"])
        if not n or not p or r["parent"] not in n["parents"]:
            errs.append(f"recognition {r['hash'][:12]}: names a node or parent that does not match")
            continue
        if r["by_orcid"] != p["contributor"]["orcid"]:
            errs.append(f"recognition {r['hash'][:12]}: signed by {r['by_orcid']}, but the parent belongs to {p['contributor']['orcid']}")
            continue
        if not doi_ok(r["record_doi"]):
            errs.append(f"recognition {r['hash'][:12]}: needs a deposit DOI")
            continue
        recs.setdefault(r["node"], set()).add(r["parent"])
    status = {}
    for n in nodes:
        h = n["hash"]
        if n["kind"] == "root":
            status[h] = "root"
            continue
        why = []
        if set(n["parents"]) - recs.get(h, set()):
            why.append("not countersigned by every parent")
        if any(status.get(p) not in ("root", "recognized") for p in n["parents"]):
            why.append("a parent is not recognized")
        if n["root_claims_touched"] and not n["assignment_ref"]:
            why.append("touches a root claim with no recorded assignment (E.8)")
        if not doi_ok(n["record_doi"]):
            why.append("no deposit DOI")
        status[h] = "recognized" if not why else "fork: " + "; ".join(why)
    def ancestry(h, seen=None):
        seen = seen if seen is not None else set()
        if h in seen:
            return seen
        seen.add(h)
        for p in by[h]["parents"]:
            ancestry(p, seen)
        return seen
    for n in nodes:
        anc = ancestry(n["hash"])
        total = sum(float(by[x]["pool_share_pct"]) for x in anc if status.get(x) == "recognized")
        if pool_cap is not None and total > pool_cap + 1e-9:
            errs.append(f"{n['hash'][:12]}: pool shares in its ancestry total {total:g}%, over the {pool_cap:g}% cap (E.7)")
    return errs, warn, status, by, ancestry

def cmd_verify(a, g):
    data = load(a.lineage)
    cap = a.pool_cap
    if a.license:
        vals = g.parse_header(open(a.license, encoding="utf-8").read())
        if cap is None and vals.get("POOL_CAP_PCT"):
            cap = float(vals["POOL_CAP_PCT"])
        root = data["nodes"][0]
        for key, field in (("INVENTOR_ORCID", root["contributor"]["orcid"]), ("INVENTOR_NAME", root["contributor"]["name"]),
                           ("INVENTOR_RECORD_DOI", root["record_doi"])):
            if vals.get(key) and vals[key] != field:
                print(f"NOT VALID: root {key} '{field}' does not match the license '{vals[key]}' (Section I is locked)")
                sys.exit(1)
    errs, warn, status, by, _ = analyze(data, g, cap)
    print(f"{'node':14} {'contributor':28} {'terms':12} {'pool':>6}  status")
    for n in data["nodes"]:
        print(f"{n['hash'][:12]:14} {n['contributor']['name'][:27]:28} {n['terms']:12} {n['pool_share_pct']+'%':>6}  {status[n['hash']]}")
    for w in warn:
        print("note: " + w)
    if errs:
        print("NOT VALID:\n  " + "\n  ".join(errs))
        sys.exit(1)
    print("VALID lineage." + (f" Pool cap {cap:g}% holds on every path." if cap is not None else " Pool cap not checked (no --license or --pool-cap)."))

def cmd_path(a, g):
    data = load(a.lineage)
    errs, warn, status, by, ancestry = analyze(data, g, None)
    target = find(data, a.node)
    anc = ancestry(target["hash"])
    order = [n for n in data["nodes"] if n["hash"] in anc]
    root = data["nodes"][0]
    print(f"Original inventor: {root['contributor']['name']} (ORCID {root['contributor']['orcid']}), Inventor Record DOI {root['record_doi']}")
    for n in order[1:]:
        label = "Enriched by" if status[n["hash"]] == "recognized" else "Fork by"
        print(f"{label}: {n['contributor']['name']} (ORCID {n['contributor']['orcid']}), lineage node {n['hash'][:12]}, Record DOI {n['record_doi']}")
    print("\nTerms by portion (each applies only to its own scope):")
    print(f"  root: Greater Good License 1.0, Parts S, W, P as declared")
    for n in order[1:]:
        extra = f" at {n['reserved_price_url']}" if n["terms"] == "reserved" else ""
        print(f"  {n['hash'][:12]} {n['scope']['description']}: {n['terms']}{extra} [{status[n['hash']]}]")
    pool = sum(float(n["pool_share_pct"]) for n in order if status[n["hash"]] == "recognized")
    print(f"\nPool shares paid from the root fee for this path: {pool:g}%")

def main(argv, g):
    ap = argparse.ArgumentParser(prog="ggl.py lineage")
    sp = ap.add_subparsers(dest="action", required=True)
    i = sp.add_parser("init"); i.add_argument("params"); i.add_argument("-o", "--out", default="LINEAGE.json")
    i.add_argument("--material"); i.add_argument("--date")
    d = sp.add_parser("add"); d.add_argument("lineage")
    for f in ("--name", "--orcid", "--parents", "--version", "--description", "--terms", "--doi"):
        d.add_argument(f, required=True)
    for f in ("--work", "--sections", "--claims", "--material", "--material-sha", "--price-url", "--pool-share", "--assignment", "--date"):
        d.add_argument(f)
    d.add_argument("--enrichment-line", action="store_true"); d.add_argument("--touches-root-claims", action="store_true")
    r = sp.add_parser("recognize"); r.add_argument("lineage")
    for f in ("--node", "--parent", "--by-orcid", "--doi"):
        r.add_argument(f, required=True)
    r.add_argument("--date")
    v = sp.add_parser("verify"); v.add_argument("lineage"); v.add_argument("--license"); v.add_argument("--pool-cap", type=float)
    p = sp.add_parser("path"); p.add_argument("lineage"); p.add_argument("node")
    a = ap.parse_args(argv)
    {"init": cmd_init, "add": cmd_add, "recognize": cmd_recognize, "verify": cmd_verify, "path": cmd_path}[a.action](a, g)
