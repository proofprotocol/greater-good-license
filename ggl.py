#!/usr/bin/env python3
"""Greater Good License family tool.

  ggl.py new    VARIANT -o FILE      start a parameter file (VARIANT: OS, EGR, or C)
  ggl.py check  FILE                 validate the parameter header
  ggl.py render FILE [-o OUT] [--draft]
                                     fill the canonical license text from FILE's header
  ggl.py verify FILE                 confirm a rendered license is canonical text
  ggl.py lineage ...                 Section E lineage tree (see lineage.py)
"""
import argparse, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = "<!-- GGL-PARAMS:BEGIN -->", "<!-- GGL-PARAMS:END -->"
BODY_MARK = "<!-- GGL-1.0 BODY: canonical text, do not edit below this line -->"
VARIANTS = {"OS": "GGL-OS-1.0", "EGR": "GGL-EGR-1.0", "C": "GGL-C-1.0"}
NAMES = {"GGL-OS-1.0": "Greater Good Open Source License 1.0",
         "GGL-EGR-1.0": "Greater Good Education, Government, and Research License 1.0",
         "GGL-C-1.0": "Greater Good Commercial License 1.0"}
LOCKED = ("INVENTOR_NAME", "INVENTOR_ORCID", "INVENTOR_RECORD_DOI")

def load_spec(variant=None):
    out = []
    for line in open(os.path.join(HERE, "params.spec"), encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            v, g, k, r, d = line.rstrip("\n").split("|", 4)
            if variant is None or v == "all" or VARIANTS.get(v) == variant:
                out.append((g, k, r, d))
    return out

def rules(variant=None):
    return {k: r for g, k, r, d in load_spec(variant)}

def body_template(variant):
    if variant not in NAMES:
        sys.exit(f"GGL_VARIANT must be one of {', '.join(NAMES)}")
    return open(os.path.join(HERE, "templates", f"{variant}.body"), encoding="utf-8").read()

def body_sha(variant):
    return hashlib.sha256(body_template(variant).encode("utf-8")).hexdigest()

def parse_header(text):
    if BEGIN not in text or END not in text:
        sys.exit("no GGL-PARAMS header found")
    vals = {}
    for line in text.split(BEGIN, 1)[1].split(END, 1)[0].splitlines():
        m = re.match(r'^([A-Z0-9_]+)="((?:[^"\\]|\\.)*)"', line.strip())
        if m:
            vals[m.group(1)] = m.group(2).replace('\\"', '"')
    return vals

def orcid_ok(v):
    if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", v):
        return False
    d = v.replace("-", "")
    total = 0
    for ch in d[:-1]:
        total = (total + int(ch)) * 2
    c = (12 - total % 11) % 11
    return d[-1] == ("X" if c == 10 else str(c))

def check_value(rule, v, variant=None):
    if not v or re.search(r"\bTBD\b|XXXX|\[\$?X\]|<.*?>", v, re.I):
        return "empty or placeholder"
    num = v.replace(",", "")
    if rule == "text":
        return None
    if rule == "year":
        return None if re.fullmatch(r"20\d\d", v) else "must be a year like 2026"
    if rule == "int":
        return None if re.fullmatch(r"[1-9]\d*", num) else "must be a positive whole number"
    if rule == "money":
        return None if re.fullmatch(r"\d+(\.\d{1,2})?", num) and float(num) > 0 else "must be a positive dollar amount"
    if rule == "pct":
        return None if re.fullmatch(r"\d+(\.\d+)?", v) and 0 < float(v) <= 100 else "must be a percent between 0 and 100"
    if rule == "semver":
        return None if re.fullmatch(r"\d+\.\d+\.\d+", v) else "must be x.y.z"
    if rule == "url":
        return None if re.fullmatch(r"https://\S+\.\S+", v) else "must be an https URL"
    if rule == "contact":
        return None if re.fullmatch(r"[^@\s]+@[^@\s]+\.\w+|https://\S+\.\S+", v) else "must be an email or https URL"
    if rule == "orcid":
        return None if orcid_ok(v) else "not a valid ORCID iD (format or checksum)"
    if rule == "doi":
        return None if re.fullmatch(r"10\.\d{4,9}/\S+", v) else "must be a DOI like 10.5281/zenodo.12345678"
    if rule == "offered":
        items = [x.strip() for x in v.split(",")]
        bad = [x for x in items if x not in NAMES]
        if bad:
            return "unknown license(s): " + ", ".join(bad)
        if variant and variant not in items:
            return f"must include {variant}, the license this copy is"
        return None
    if rule.startswith("enum:"):
        opts = rule[5:].split(",")
        return None if v in opts else "must be one of: " + " | ".join(opts)
    return "unknown rule"

def validate(vals):
    variant = vals.get("GGL_VARIANT")
    if variant not in NAMES:
        return [f"GGL_VARIANT: must be one of {', '.join(NAMES)}"]
    errors = []
    for g, k, r, d in load_spec(variant):
        err = check_value(r, vals.get(k, ""), variant)
        if err:
            errors.append(f"{k}: {err}")
    if variant == "GGL-C-1.0":
        try:
            if float(vals["ANNUAL_CAP_USD"].replace(",", "")) < float(vals["MIN_ANNUAL_FEE_USD"].replace(",", "")):
                errors.append("ANNUAL_CAP_USD: must be at least MIN_ANNUAL_FEE_USD")
        except (KeyError, ValueError):
            pass
    return errors

def fill(body, vals, variant):
    rl = rules(variant)
    def sub(m):
        k = m.group(1)
        v = vals.get(k, "")
        return f"[[UNFILLED: {k}]]" if check_value(rl.get(k, "text"), v, variant) else v
    return re.sub(r"\{\{([A-Z_]+)\}\}", sub, body)

def header(vals, variant, draft):
    lines = [BEGIN, "```bash",
             f"# {NAMES[variant]} PARAMETERS. Every value is REQUIRED for this license to be valid.",
             "# LOCKED values never change once set for a Covered Work (Section I).",
             "# Check: python3 ggl.py check <this file>",
             f'GGL_VARIANT="{variant}"',
             f'GGL_BODY_SHA256="{body_sha(variant)}"']
    group = None
    for g, k, r, d in load_spec(variant):
        if g != group:
            lines.append(f"\n# {g}")
            group = g
        v = vals.get(k, "").replace('"', '\\"')
        lines.append(f'{k}="{v}"'.ljust(48) + f"  # {d}")
    lines += ["```", END]
    banner = ("> **DRAFT. NOT A VALID LICENSE.** Values marked UNFILLED must be completed and the file must pass `ggl.py check`.\n\n"
              if draft else "")
    return banner + "\n".join(lines) + "\n"

def template_text(variant, vals=None, title=None):
    vals = vals or {}
    intro = (f"# {title or NAMES[variant] + ': Template'}\n\n"
             "Fill every value in the parameter block below, then run `python3 ggl.py render <this file> -o LICENSE.md`.\n"
             "A license with any empty or placeholder value is not valid. `ggl.py check` lists what is missing.\n"
             "Do not edit the text below the body line. Only the parameters change from one license to the next.\n\n")
    return intro + header(vals, variant, False) + "\n" + BODY_MARK + body_template(variant)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "lineage":
        sys.path.insert(0, HERE)
        import lineage
        lineage.main(sys.argv[2:], sys.modules[__name__])
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["new", "check", "render", "verify"])
    ap.add_argument("file")
    ap.add_argument("-o", "--out")
    ap.add_argument("--draft", action="store_true")
    a = ap.parse_args()
    if a.cmd == "new":
        variant = VARIANTS.get(a.file.upper(), a.file)
        if variant not in NAMES:
            sys.exit("VARIANT must be OS, EGR, or C")
        open(a.out or f"{variant}.ggl.md", "w", encoding="utf-8").write(template_text(variant))
        print(f"wrote {a.out or variant + '.ggl.md'}")
        return
    text = open(a.file, encoding="utf-8").read()
    vals = parse_header(text)
    variant = vals.get("GGL_VARIANT")
    errors = validate(vals)
    if a.cmd == "check":
        if errors:
            print("NOT VALID. Fill these:\n  " + "\n  ".join(errors))
            sys.exit(1)
        print(f"VALID {variant}: every required parameter is filled.")
        return
    if variant not in NAMES:
        sys.exit("GGL_VARIANT missing or unknown")
    if a.cmd == "render":
        if errors and not a.draft:
            print("Refusing to render a license with missing values:\n  " + "\n  ".join(errors), file=sys.stderr)
            print("Use --draft to render with UNFILLED markers.", file=sys.stderr)
            sys.exit(1)
        out = header(vals, variant, bool(errors)) + "\n" + BODY_MARK + fill(body_template(variant), vals, variant)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(out)
            print(("DRAFT written to " if errors else "Valid license written to ") + a.out)
        else:
            sys.stdout.write(out)
        return
    if a.cmd == "verify":
        if BODY_MARK not in text:
            sys.exit("not a rendered GGL file")
        if text.split(BODY_MARK, 1)[1] != fill(body_template(variant), vals, variant):
            print(f"ALTERED: the license text differs from canonical {variant} with these parameters.")
            sys.exit(2)
        if vals.get("GGL_BODY_SHA256") != body_sha(variant):
            print(f"ALTERED: body hash in header does not match canonical {variant}.")
            sys.exit(2)
        print(f"VERIFIED: canonical {variant} text; only parameters differ." + (" Parameters incomplete: " + "; ".join(errors) if errors else ""))

if __name__ == "__main__":
    main()
