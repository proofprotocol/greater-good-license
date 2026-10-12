#!/usr/bin/env python3
"""Contribution Markers for the Greater Good License 1.0, Section M.

  python3 ggl_contrib.py check   FILE                       validate markers (M.5); exit 1 if void
  python3 ggl_contrib.py list    FILE                       list orgs and blocks
  python3 ggl_contrib.py extract FILE --org NAME [-o OUT]   Contribution Extract for one organization (M.9)
  python3 ggl_contrib.py verify  EXTRACT --source FILE      confirm an extract matches its source
  python3 ggl_contrib.py schedule SCHEDULE.json [--root DIR] validate a Contribution Schedule against the files (M.4)
  python3 ggl_contrib.py extract-json FILE --pointer P      extract one JSON element by JSON Pointer (M.2a)

The Contribution Schedule (contributions.json) is the authority: markers or pointers for an
organization with no Schedule entry contribute nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# The marker is the bracketed text only; optional comment wrappers around it are tolerated (M.2).
_WRAP = r"^\s*(?:#|//|--|;|%|\*|/\*|<!--)?\s*"
_TAIL = r"\s*(?:\*/|-->)?\s*$"
START = re.compile(_WRAP + r"\[CONTRIBUTED TO (?P<org>[^\]\r\n]+)\]" + _TAIL)
END = re.compile(_WRAP + r"\[/END OF CONTRIBUTED TO (?P<org>[^\]\r\n]+)\]" + _TAIL)


@dataclass
class Block:
    org: str
    start_line: int          # 1-based line of the start marker
    end_line: int            # 1-based line of the end marker
    lines: List[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "".join(self.lines)


@dataclass
class Result:
    blocks: List[Block]
    errors: List[str]

    @property
    def void(self) -> bool:
        return bool(self.errors)


def parse(text: str) -> Result:
    lines = text.splitlines(keepends=True)
    stack: List[Tuple[str, int]] = []
    open_bufs: Dict[int, List[str]] = {}
    blocks: List[Block] = []
    errors: List[str] = []
    for i, line in enumerate(lines, start=1):
        m_s, m_e = START.match(line), END.match(line)
        if m_s:
            org = m_s.group("org")
            if any(o == org for o, _ in stack):
                errors.append(f"line {i}: '{org}' nested inside its own block (M.5)")
            stack.append((org, i))
            open_bufs[i] = []
            continue
        if m_e:
            org = m_e.group("org")
            if not stack:
                errors.append(f"line {i}: end marker for '{org}' with no start (M.5)")
                continue
            top_org, top_line = stack[-1]
            if top_org != org:
                if any(o == org for o, _ in stack):
                    errors.append(f"line {i}: block '{org}' crosses block '{top_org}' (M.5)")
                else:
                    errors.append(f"line {i}: end marker '{org}' does not match open '{top_org}' (M.5)")
                continue
            stack.pop()
            blocks.append(Block(org, top_line, i, open_bufs.pop(top_line)))
            continue
        for buf in open_bufs.values():
            buf.append(line)
    for org, ln in stack:
        errors.append(f"line {ln}: start marker for '{org}' never closed (M.5)")
    blocks.sort(key=lambda b: b.start_line)
    return Result(blocks, errors)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract(source_text: str, source_name: str, org: str, version: str = "",
            register: Optional[dict] = None) -> str:
    res = parse(source_text)
    if res.void:
        raise ValueError("markers are void under M.5; nothing is contributed: " + "; ".join(res.errors))
    mine = [b for b in res.blocks if b.org == org]
    if not mine:
        raise ValueError(f"no blocks contributed to '{org}'")
    if register is not None and not any(e.get("organization") == org for e in register.get("entries", [])):
        raise ValueError(f"'{org}' has no Contribution Schedule entry; markers contribute nothing (M.4)")
    header = {
        "ggl": "1.0", "section": "C", "organization": org, "source": source_name, "version": version,
        "source_sha256": sha256(source_text.encode("utf-8")),
        "blocks": [{"start_line": b.start_line, "end_line": b.end_line, "sha256": sha256(b.text.encode("utf-8"))} for b in mine],
    }
    body = []
    for b in mine:
        body.append(f"[CONTRIBUTED TO {org}]\n{b.text}[/END OF CONTRIBUTED TO {org}]\n")
    return ("<!-- GGL-1.0 Contribution Extract\n" + json.dumps(header, indent=2) + "\n-->\n\n"
            "Everything below was contributed to " + org + " under the Contribution Schedule entry for "
            "this version. Section I (Original Inventor), the Inventor Line, and Part S attribution apply.\n\n"
            + "\n".join(body))


def verify(extract_text: str, source_text: str) -> List[str]:
    m = re.search(r"<!-- GGL-1.0 Contribution Extract\n(\{.*?\})\n-->", extract_text, re.S)
    if not m:
        return ["not a Contribution Extract"]
    h = json.loads(m.group(1))
    problems = []
    if h["source_sha256"] != sha256(source_text.encode("utf-8")):
        problems.append("source does not match the hash recorded in the extract")
    res = parse(source_text)
    if res.void:
        problems.append("source markers are void under M.5")
    mine = [b for b in res.blocks if b.org == h["organization"]]
    got = [{"start_line": b.start_line, "end_line": b.end_line, "sha256": sha256(b.text.encode("utf-8"))} for b in mine]
    if got != h["blocks"]:
        problems.append("blocks in the extract do not match the blocks in the source")
    return problems


# ---------------------------------------------------------------- Schedule and JSON (M.2a, M.4)

def json_pointer(doc, pointer: str):
    """RFC 6901."""
    if pointer in ("", "/"):
        return doc
    if not pointer.startswith("/"):
        raise ValueError(f"not a JSON Pointer: {pointer!r}")
    cur = doc
    for raw in pointer[1:].split("/"):
        tok = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(tok)]
        elif isinstance(cur, dict):
            if tok not in cur:
                raise KeyError(f"pointer {pointer!r}: no member {tok!r}")
            cur = cur[tok]
        else:
            raise KeyError(f"pointer {pointer!r}: cannot descend into a scalar")
    return cur


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def check_schedule(schedule: dict, root: str = ".") -> List[str]:
    """M.4: every entry well formed; every listed file exists; markers present where claimed;
    pointers resolve; YAML entries are listed (markers alone are not authority); and every
    organization named in markers in a listed file has an entry."""
    import os
    problems: List[str] = []
    entries = schedule.get("entries", [])
    req = ("organization", "work", "version", "scope", "terms", "patent_claims", "date", "signature")
    orgs = set()
    for n, e in enumerate(entries):
        miss = [k for k in req if k not in e]
        if miss:
            problems.append(f"entry {n}: missing {miss}")
            continue
        orgs.add(e["organization"])
        for sc in e["scope"]:
            path = os.path.join(root, sc["file"])
            if not os.path.exists(path):
                problems.append(f"entry {n}: file not found: {sc['file']}")
                continue
            by = sc.get("by")
            text = open(path, encoding="utf-8").read()
            if by == "markers":
                if sc["file"].endswith(".json"):
                    problems.append(f"entry {n}: {sc['file']} is JSON; markers are impossible, use by: pointer (M.2a)")
                    continue
                res = parse(text)
                if res.void:
                    problems.append(f"entry {n}: {sc['file']} markers void: " + "; ".join(res.errors))
                elif not any(b.org == e["organization"] for b in res.blocks):
                    problems.append(f"entry {n}: no '{e['organization']}' markers in {sc['file']}")
            elif by == "pointer":
                if not sc["file"].endswith(".json"):
                    problems.append(f"entry {n}: by: pointer is for JSON files; YAML uses by: node")
                    continue
                try:
                    json_pointer(json.loads(text), sc["pointer"])
                except Exception as ex:
                    problems.append(f"entry {n}: {sc['file']} {ex}")
            elif by == "node":
                if not sc["file"].endswith((".yaml", ".yml")):
                    problems.append(f"entry {n}: by: node is for YAML files")
                if not sc.get("node"):
                    problems.append(f"entry {n}: by: node needs a node path")
            elif by == "whole_file":
                pass
            else:
                problems.append(f"entry {n}: unknown scope kind {by!r}")
    # markers for organizations that have no entry contribute nothing: report them
    listed = {sc["file"] for e in entries if "scope" in e for sc in e["scope"]}
    for f in sorted(listed):
        path = os.path.join(root, f)
        if os.path.exists(path) and not f.endswith(".json"):
            for b in parse(open(path, encoding="utf-8").read()).blocks:
                if b.org not in orgs:
                    problems.append(f"{f} lines {b.start_line}-{b.end_line}: markers for '{b.org}' with no Schedule entry contribute nothing")
    return problems


def extract_json(text: str, source_name: str, pointer: str, org: str = "") -> str:
    doc = json.loads(text)
    el = json_pointer(doc, pointer)
    out = {"ggl": "1.0", "section": "M.2a", "organization": org, "source": source_name, "pointer": pointer,
           "source_sha256": sha256(text.encode("utf-8")), "element_sha256": sha256(canonical(el)), "element": el}
    return json.dumps(out, indent=2) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("check", "list"):
        p = sub.add_parser(c); p.add_argument("file")
    p = sub.add_parser("extract"); p.add_argument("file"); p.add_argument("--org", required=True)
    p.add_argument("--version", default=""); p.add_argument("--register"); p.add_argument("-o", "--out")
    p = sub.add_parser("verify"); p.add_argument("extract"); p.add_argument("--source", required=True)
    p = sub.add_parser("schedule"); p.add_argument("schedule"); p.add_argument("--root", default=".")
    p = sub.add_parser("extract-json"); p.add_argument("file"); p.add_argument("--pointer", required=True); p.add_argument("--org", default="")
    a = ap.parse_args(argv)
    if a.cmd == "schedule":
        probs = check_schedule(json.load(open(a.schedule)), a.root)
        print("ok" if not probs else "PROBLEMS:\n  " + "\n  ".join(probs)); return 1 if probs else 0
    if a.cmd == "extract-json":
        sys.stdout.write(extract_json(open(a.file, encoding="utf-8").read(), a.file, a.pointer, a.org)); return 0
    if a.cmd in ("check", "list"):
        res = parse(open(a.file, encoding="utf-8").read())
        if res.void:
            print("VOID (nothing contributed):"); [print("  " + e) for e in res.errors]; return 1
        if a.cmd == "check":
            print(f"ok: {len(res.blocks)} block(s), organizations: {sorted({b.org for b in res.blocks}) or 'none'}"); return 0
        for b in res.blocks:
            print(f"{b.org}\tlines {b.start_line}-{b.end_line}\t{len(b.lines)} line(s)")
        return 0
    if a.cmd == "extract":
        reg = json.load(open(a.register)) if a.register else None
        out = extract(open(a.file, encoding="utf-8").read(), a.file, a.org, a.version, reg)
        (open(a.out, "w", encoding="utf-8").write(out) if a.out else sys.stdout.write(out)); return 0
    probs = verify(open(a.extract, encoding="utf-8").read(), open(a.source, encoding="utf-8").read())
    print("verified" if not probs else "FAILED: " + "; ".join(probs)); return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
