# Greater Good License family, version 1.0

Three licenses, one shared core.

| License | SPDX | For | Cost |
|---|---|---|---|
| Greater Good Open Source License 1.0 | `LicenseRef-GGL-OS-1.0` | Anyone, for Software released as open source | Free. Share-alike, including network use. |
| Greater Good Education, Government, and Research License 1.0 | `LicenseRef-GGL-EGR-1.0` | Schools, governments, research and nonprofit bodies, and individuals learning | Free. Non-commercial. |
| Greater Good Commercial License 1.0 | `LicenseRef-GGL-C-1.0` | Commercial use outside the other two | Fee. Waived for small businesses (Startup Tier). |

All three share Section I (Original Inventor), Part S (spec text, CC BY 4.0 by default), Part P (patents: Contributed and Reserved claims), Section E (Enrichment and Lineage), and Section G, word for word. Each adds its own part: O, R, or C. Each Covered Work declares which of the three it is offered under.

## Files

| Path | What it is |
|---|---|
| `templates/GGL-*-1.0-TEMPLATE.md` | The three templates. Parameter block at the top, canonical text below the body line. |
| `templates/GGL-*-1.0.body` | The canonical license texts that `verify` checks against. |
| `PP-SPEC-077.GGL-*-1.0.ggl.md` | Proof Protocol's values filled in for PP-SPEC-077, one per license. |
| `LICENSE-PP-SPEC-077.GGL-*-1.0.md` | Rendered licenses for PP-SPEC-077. Marked DRAFT until the open values are filled. |
| `ggl.py`, `params.spec` | Checker and renderer. `params.spec` lists each parameter, its rule, and which licenses use it. |
| `lineage.py` | Section E lineage tool, run as `ggl.py lineage`. |
| `build.py`, `blocks/` | Rebuild the three texts from the shared blocks. Only needed to change the license text itself. |
| `PATENT-SCHEDULE-TEMPLATE.md` | Template for the Part P Patent Schedule. |
| `inventor-record/` | The Zenodo Inventor Record. Upload this first. |
| `examples/LINEAGE.example.json` | Demo tree with made-up people and DOIs, left failing so `verify` shows every check. |

## Use

```bash
python3 ggl.py new C -o MY-WORK.ggl.md              # OS, EGR, or C
python3 ggl.py check  MY-WORK.ggl.md                # lists anything empty, malformed, or a placeholder
python3 ggl.py render MY-WORK.ggl.md -o LICENSE.md  # refuses until every value passes; --draft marks gaps
python3 ggl.py verify LICENSE.md                    # any edit to the license text fails
```

Parameters marked LOCKED (inventor name, ORCID, Inventor Record DOI) never change once set for a Covered Work. OS and EGR use 23 parameters; C adds 12 for fees and terms.

## Lineage (Section E)

```bash
python3 ggl.py lineage init PP-SPEC-077.GGL-C-1.0.ggl.md -o LINEAGE.json --material SPEC.md
python3 ggl.py lineage add LINEAGE.json --name "Jane Doe" --orcid 0000-0000-0000-0000 \
    --parents <root hash> --version 0.8.0 --sections 17.10 --description "Cloud profile" \
    --terms contributed --pool-share 10 --material profile.md --doi 10.5281/zenodo.NNNNNNNN
python3 ggl.py lineage recognize LINEAGE.json --node <jane hash> --parent <root hash> \
    --by-orcid 0009-0004-1058-7666 --doi 10.5281/zenodo.NNNNNNNN
python3 ggl.py lineage verify LINEAGE.json --license PP-SPEC-077.GGL-C-1.0.ggl.md
python3 ggl.py lineage path   LINEAGE.json <node hash>
```

`init` needs a real Inventor Record DOI, so run it after the Zenodo deposit.
