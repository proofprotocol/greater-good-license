import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from ggl_contrib import parse, extract, verify

DOC = """# Spec
intro, not contributed
[CONTRIBUTED TO Proof-of-Control Initiative]
## Definitions
term A
[/END OF CONTRIBUTED TO Proof-of-Control Initiative]
held back
<!-- [CONTRIBUTED TO OWASP Foundation] -->
schema text
<!-- [/END OF CONTRIBUTED TO OWASP Foundation] -->
"""

def test_default_is_nothing_contributed():
    r = parse("plain text\nno markers\n")
    assert not r.void and r.blocks == []

def test_blocks_found_per_org_and_comment_wrappers_tolerated():
    r = parse(DOC)
    assert not r.void
    assert [(b.org, b.start_line, b.end_line) for b in r.blocks] == [("Proof-of-Control Initiative", 3, 6), ("OWASP Foundation", 8, 10)]
    assert r.blocks[0].text == "## Definitions\nterm A\n"

def test_code_comment_markers():
    code = "x=1\n# [CONTRIBUTED TO Acme]\ndef f():\n    return 2\n# [/END OF CONTRIBUTED TO Acme]\n"
    r = parse(code); assert not r.void and r.blocks[0].text.startswith("def f")

@pytest.mark.parametrize("bad", [
    "[CONTRIBUTED TO A]\ntext\n",                                              # never closed
    "text\n[/END OF CONTRIBUTED TO A]\n",                                       # no start
    "[CONTRIBUTED TO A]\nx\n[/END OF CONTRIBUTED TO B]\n",                      # name mismatch
    "[CONTRIBUTED TO A]\n[CONTRIBUTED TO A]\nx\n[/END OF CONTRIBUTED TO A]\n[/END OF CONTRIBUTED TO A]\n",  # same org nested
    "[CONTRIBUTED TO A]\n[CONTRIBUTED TO B]\nx\n[/END OF CONTRIBUTED TO A]\n[/END OF CONTRIBUTED TO B]\n",  # crossing
    "[CONTRIBUTED TO a]\nx\n[/END OF CONTRIBUTED TO A]\n",                      # case differs
])
def test_fail_closed(bad):
    assert parse(bad).void

def test_different_orgs_may_nest():
    t = "[CONTRIBUTED TO A]\nouter\n[CONTRIBUTED TO B]\ninner\n[/END OF CONTRIBUTED TO B]\n[/END OF CONTRIBUTED TO A]\n"
    r = parse(t); assert not r.void
    a = [b for b in r.blocks if b.org == "A"][0]; b = [b for b in r.blocks if b.org == "B"][0]
    assert "inner" in a.text and "outer" not in b.text

def test_extract_contains_only_that_org_and_verifies():
    reg = {"entries": [{"organization": "Proof-of-Control Initiative"}]}  # Schedule (M.4)
    ex = extract(DOC, "SPEC.md", "Proof-of-Control Initiative", "0.7.2", reg)
    assert "term A" in ex and "held back" not in ex and "schema text" not in ex
    assert verify(ex, DOC) == []
    assert verify(ex, DOC.replace("term A", "term B"))   # tampered source fails

def test_no_register_entry_contributes_nothing():
    with pytest.raises(ValueError):
        extract(DOC, "SPEC.md", "OWASP Foundation", "0.7.2", {"entries": []})

def test_void_file_cannot_be_extracted():
    with pytest.raises(ValueError):
        extract("[CONTRIBUTED TO A]\nx\n", "f", "A")


# ---------------- Contribution Schedule (M.4) and formats without markers (M.2a)
import json, tempfile
import jsonschema
from ggl_contrib import check_schedule, extract_json, json_pointer

SCHEMA = json.load(open(os.path.join(os.path.dirname(__file__), "..", "contributions.schema.json")))

def _repo(files):
    d = tempfile.mkdtemp()
    for name, body in files.items():
        p = os.path.join(d, name); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(body)
    return d

def _entry(org, scope):
    return {"organization": org, "work": "PP-SPEC-077", "version": "0.7.2", "scope": scope,
            "terms": {"agreement_record_id": "ab" * 32}, "patent_claims": [], "date": "2026-10-20", "signature": "sig"}

UOP = json.dumps({"properties": {"holder": {"type": "object"}, "secret": {"type": "string"}}})

def test_schedule_valid_for_markers_and_json_pointer():
    d = _repo({"SPEC.md": DOC, "schemas/uop.schema.json": UOP})
    sch = {"ggl": "1.0", "work": "PP-SPEC-077", "entries": [
        _entry("Proof-of-Control Initiative", [{"file": "SPEC.md", "by": "markers"},
                                               {"file": "schemas/uop.schema.json", "by": "pointer", "pointer": "/properties/holder"}]),
        _entry("OWASP Foundation", [{"file": "SPEC.md", "by": "markers"}])]}
    jsonschema.validate(sch, SCHEMA)
    assert check_schedule(sch, d) == []

def test_markers_without_schedule_entry_are_reported():
    d = _repo({"SPEC.md": DOC})
    sch = {"ggl": "1.0", "work": "x", "entries": [_entry("Proof-of-Control Initiative", [{"file": "SPEC.md", "by": "markers"}])]}
    probs = check_schedule(sch, d)
    assert any("OWASP Foundation" in p and "no Schedule entry" in p for p in probs)

def test_json_cannot_use_markers_and_bad_pointer_fails():
    d = _repo({"a.json": UOP})
    assert check_schedule({"entries": [_entry("X", [{"file": "a.json", "by": "markers"}])]}, d)
    assert check_schedule({"entries": [_entry("X", [{"file": "a.json", "by": "pointer", "pointer": "/properties/nope"}])]}, d)

def test_yaml_needs_node_path():
    d = _repo({"p.yaml": "# [CONTRIBUTED TO X]\na: 1\n# [/END OF CONTRIBUTED TO X]\n"})
    assert check_schedule({"entries": [_entry("X", [{"file": "p.yaml", "by": "node"}])]}, d)
    assert check_schedule({"entries": [_entry("X", [{"file": "p.yaml", "by": "node", "node": "a"}])]}, d) == []

def test_json_pointer_rfc6901_and_extract():
    doc = {"a/b": {"m~n": [10, 20]}}
    assert json_pointer(doc, "/a~1b/m~0n/1") == 20
    ex = json.loads(extract_json(UOP, "uop.schema.json", "/properties/holder", "OWASP Foundation"))
    assert ex["element"] == {"type": "object"} and "secret" not in json.dumps(ex)
    assert len(ex["element_sha256"]) == 64 and len(ex["source_sha256"]) == 64
