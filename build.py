#!/usr/bin/env python3
"""Builds the three Greater Good License family templates from shared blocks."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
B = lambda n: open(os.path.join(HERE, "blocks", n), encoding="utf-8").read().strip()
BODY_MARK = "<!-- GGL-1.0 BODY: canonical text, do not edit below this line -->"

VARIANTS = {
 "OS":  ("GGL-OS-1.0",  "The Greater Good Open Source License, Version 1.0", "Open for everyone. Credit to the people who built it."),
 "EGR": ("GGL-EGR-1.0", "The Greater Good Education, Government, and Research License, Version 1.0", "Free for teaching, public service, and discovery."),
 "C":   ("GGL-C-1.0",   "The Greater Good Commercial License, Version 1.0", "Fair terms for those who profit, so the public-good work stays funded."),
}

def common_head(v):
    spdx, name, tag = VARIANTS[v]
    return f"""# {name} ({spdx})

*{tag}*

SPDX identifier: `LicenseRef-{spdx}`

Licensor: {{{{LICENSOR_NAME}}}}, {{{{LICENSOR_LOCATION}}}}.

Original Inventor: {{{{INVENTOR_NAME}}}}, ORCID {{{{INVENTOR_ORCID}}}}. Inventor Record: DOI {{{{INVENTOR_RECORD_DOI}}}}. See Section I. This line is permanent.

Required Notice: Copyright {{{{COPYRIGHT_YEAR}}}} {{{{LICENSOR_NAME}}}}. Licensed under the {name.replace(', Version 1.0',' 1.0')}. Original inventor: {{{{INVENTOR_NAME}}}} (ORCID {{{{INVENTOR_ORCID}}}}), Inventor Record DOI {{{{INVENTOR_RECORD_DOI}}}}. Licensing contact: {{{{LICENSING_CONTACT}}}}.

---

## 0. The Greater Good License Family

| License | For | Cost |
|---|---|---|
| **GGL-OS-1.0**, Open Source | Anyone, for Software the Licensor releases as open source | Free. Share-alike. |
| **GGL-EGR-1.0**, Education, Government, and Research | Schools, governments, and research and nonprofit bodies | Free. Non-commercial. |
| **GGL-C-1.0**, Commercial | Anyone using Covered Works commercially outside the other two | Fee. Waived for small businesses. |

All three licenses share the same Section I (Original Inventor), Part S (Specification Text), Part P (Patents), Section E (Enrichment and Lineage), Section M (Contribution Markers), and Section G (General Terms), word for word. They differ only in their own Part: Part O, Part R, or Part C. This copy is **{spdx}**, and its own Part is Part {v[0]}.

**Offered licenses.** Each Covered Work's declaration lists the family licenses it is offered under. You may use it under any of those whose conditions you meet. If you meet none of them, you have no license to the Covered Work beyond Part S and P.2.

**Acceptance.** By using, copying, modifying, implementing, or distributing a Covered Work, or by claiming conformance with one, you accept the terms of the license you use it under. If you do not accept them, do not do those things.

**Declaration.** Every Covered Work carries a declaration in its header or LICENSE file in this form:

```
License family: Greater Good License 1.0
Covered Work: {{{{COVERED_WORK}}}}, version {{{{COVERED_WORK_VERSION}}}}
Offered under: {{{{OFFERED_LICENSES}}}}
Original Inventor: {{{{INVENTOR_NAME}}}}, ORCID {{{{INVENTOR_ORCID}}}}
Inventor Record: DOI {{{{INVENTOR_RECORD_DOI}}}}
Specification text: {{{{SPEC_LICENSE}}}}
Patent Schedule: {{{{PATENT_SCHEDULE}}}}, version {{{{PATENT_SCHEDULE_VERSION}}}}
```"""

def patents():
    p = B("P.md")
    p = p.replace("""**P.2 Contributed Claims.** The Licensor grants you a worldwide, royalty-free, non-exclusive license under the Contributed Claims to make, use, sell, offer for sale, import, and otherwise practice any implementation, to the extent it conforms to the Specification the claim is listed against. This license does not depend on Part W and is free for everyone, including commercial users.""",
"""**P.2 Contributed Claims.** The Licensor grants you a worldwide, royalty-free, non-exclusive license under the Contributed Claims to make, use, sell, offer for sale, import, and otherwise practice any implementation, to the extent it conforms to the Specification the claim is listed against. This license is free for everyone, including commercial users, under every license in the family.""")
    p = re.sub(r"\*\*P\.3 Reserved Claims\.\*\*.*?(?=\*\*P\.4)", """**P.3 Reserved Claims.** No license is granted under Reserved Claims except as a family license grants it in its own Part: GGL-OS-1.0 in O.6, GGL-EGR-1.0 in R.2, and GGL-C-1.0 in C.3. The Licensor will not assert Reserved Claims against an individual for personal study, or against anyone for standards review or for citing and discussing a Specification.

""", p, flags=re.S)
    p = p.replace("every license you hold under Part P ends on the date you file, and every license under Parts W and P ends for the Affiliate that files.",
                  "every license you hold under the Greater Good License family ends on the date you file, for you and for the Affiliate that files.")
    p = p.replace("a worldwide, royalty-free, non-exclusive license under that claim to use it with the Covered Works.",
                  "a worldwide, royalty-free, non-exclusive license under that claim to use it with the Covered Works.", 1)
    p = p.replace("every other licensee under this license", "every other licensee under the Greater Good License family")
    p = p.replace("Part P lets the Licensor give specific inventions to the public good while keeping others to sustain the business that maintains the protocol.",
                  "Part P lets the Licensor give specific inventions to the public good while keeping others to sustain the work that maintains the protocol.")
    assert "Part W" not in p, p
    return p

def enrichment():
    e = B("E.md")
    e = e.replace("**E.7 Royalty pool.** A licensee pays the Part W fee once, however deep the tree.",
                  "**E.7 Royalty pool.** A licensee under GGL-C-1.0 pays its fee once, however deep the tree.")
    e = e.replace("out of fees collected on works whose ancestry includes that node.",
                  "out of GGL-C-1.0 fees collected on works whose ancestry includes that node.")
    assert "Part W" not in e
    return e

def general():
    g = B("G.md")
    g = g.replace("**G.5 Definitions.** ", """**G.5 Definitions.** **Software** means the code, compiled code, schemas, test suites, test vectors, tools, and documentation the Licensor releases as part of a Covered Work, and later versions of them. **Derivative Work** means a work based on or derived from the Software: modifications, forks, translations, ports, rewrites in another language, and models trained or tuned on it. Using the Software's outputs, results, and reports is not a Derivative Work, and a component that connects at a declared Integration Point without copying, modifying, or linking in Software code is not one. An independent implementation written from a Specification alone is not a Derivative Work of the Software; Part P governs it. """)
    g = g.replace("**G.3 Termination.** If your license ends, you must stop the use that needed it, and all amounts owed remain due.",
                  "**G.3 Termination.** If your license ends, you must stop the use that needed it, and any amounts owed remain due.")
    return g

PART = {}
PART["OS"] = """## Part O. Open Source Terms

**O.1 Grant.** Anyone may use, copy, modify, and distribute the Open Source Software, for any purpose, including commercial use, at no cost, on the conditions in this license.

**O.2 Open Source Software** means the Software a Covered Work's declaration offers under GGL-OS-1.0, and Derivative Works of it.

**O.3 Share-alike.** If you distribute Open Source Software or a Derivative Work of it, you must do so under GGL-OS-1.0, include its complete corresponding source, this license, the Required Notice, and the Inventor Line, and add no further restrictions.

**O.4 Network use.** If you modify Open Source Software and let others use it over a network, you must offer those users the complete source of your modified version under GGL-OS-1.0. Hosting is allowed. Hiding changes is not.

**O.5 Your own work.** Software that only communicates with Open Source Software at a declared Integration Point, or only uses its outputs, results, and reports, is not covered by O.3.

**O.6 Patents.** The Licensor grants you a worldwide, royalty-free, non-exclusive license under every claim it holds, Contributed or Reserved, that the Open Source Software as released by the Licensor necessarily practices, to make, use, sell, offer for sale, import, and distribute it and your Derivative Works of it. The grant does not reach a Reserved Claim that a Derivative Work practices only because of what was added to it.

**O.7 Other terms.** To combine Open Source Software into a product without share-alike, or to practice Reserved Claims beyond O.6, use GGL-C-1.0.

**O.8 Open source intent.** The Licensor intends GGL-OS-1.0 to meet the Open Source Definition. The Inventor Line and notices required by Section I are attribution requirements, not limits on who may use the Software or for what."""

PART["EGR"] = """## Part R. Education, Government, and Research Terms

**R.1 Who is eligible.** You are eligible if you are:

- **An educational institution:** an accredited school, college, or university;
- **A government body** at any level: national, state, regional, local, tribal, or intergovernmental;
- **A research institution:** a nonprofit research organization or public research laboratory;
- **A nonprofit organization** acting for its public-interest mission; or
- **A student or researcher** working for one of the above, within that work; or
- **An individual** using a Covered Work for personal learning, study, or testing, not for a business.

You are not eligible for any work done for a for-profit company, funded by one in exchange for rights in the results, or delivered to one.

**R.2 Grant.** An eligible party may use, copy, modify, and share every Covered Work offered under GGL-EGR-1.0, including Software not offered as open source, and may practice the Reserved Claims, for teaching, learning, research, standards work, public administration, and protecting its own systems and data, at no cost.

**R.3 Non-commercial.** You may not sell, license, or host a Covered Work for others, or provide services with it for a fee, to anyone outside eligible parties. A government body may serve other government bodies and the public without charging for the Covered Work.

**R.4 Sharing.** You may share Covered Works and Derivative Works only with other eligible parties under GGL-EGR-1.0, or publicly under GGL-OS-1.0 where the work you started from was offered under it.

**R.5 Publication.** You may publish research results, test results, and papers freely. Where you describe a Covered Work, carry the Inventor Line. Where a Specification's method requires results to be published to its Registry, follow it.

**R.6 Going commercial.** If your work becomes commercial, through a spin-out, a sponsored deliverable, or a sale, that use needs GGL-C-1.0 or GGL-OS-1.0 from that point. A qualifying spin-out starts in the Startup Tier of GGL-C-1.0 (C.4).

**R.7 Government acquisition.** For a United States federal agency, the Covered Works are commercial computer software and commercial computer software documentation, and the agency's rights are only those in this license (FAR 12.212; DFARS 227.7202). Any other government receives the same rights, as far as its law allows.

**R.8 When eligibility ends.** If you stop being eligible, your license ends for new work. You have 90 days to move existing use to another family license.

**R.9 Authorized use only.** You may run the Software only against systems, models, and data you own or have written permission to test."""

W = B("W.md")
def wsec(tag, nxt):
    i = W.index(f"**{tag}"); j = W.index(f"**{nxt}", i) if nxt else len(W)
    return W[i:j].strip()
fees = wsec("W.3 ", "W.4 ").replace("**W.3 Commercial use: the give-back.** Everyone not covered by W.2 may use the Software for any purpose, including commercial use, by paying the Licensor each year the **greatest** of:",
                                    "**C.5 Fees: the give-back.** A commercial licensee outside the Startup Tier pays the Licensor each year the **greatest** of:")
fees = fees.replace("except as W.4 provides", "except as C.6 provides")
host = wsec("W.4 ", "W.5 ").replace("**W.4 Per user, not per host.**", "**C.6 Per user, not per host.**").replace("you pay the W.3 fee", "you pay the C.5 fee").replace("The W.3 cap", "The C.5 cap")
rep = wsec("W.7 ", "W.8 ").replace("**W.7 Reporting.**", "**C.7 Reporting.**")
fair = wsec("W.8 ", "W.9 ").replace("**W.8 Same price for everyone.**", "**C.8 Same price for everyone.**")
auth = wsec("W.9 ", None).replace("**W.9 Authorized use only.**", "**C.9 Authorized use only.**")
for s in (fees, host, rep, fair, auth):
    assert "W." not in s.replace("W.4 provides", ""), s[:80]

PART["C"] = f"""## Part C. Commercial Terms

**C.1 Who needs it.** Anyone using a Covered Work commercially who is not using it under GGL-OS-1.0 or GGL-EGR-1.0.

**C.2 Acceptance.** Commercial use outside the Startup Tier and the evaluation period requires accepting GGL-C-1.0 by a signed order form or an online acceptance that names it. Using a Covered Work commercially without doing so is still acceptance of these terms, and fees accrue from first use.

**C.3 Grant.** While you comply with Part C and your fees are paid, the Licensor grants you the right to use, copy, modify, and run the Covered Works offered under GGL-C-1.0 for any purpose; to embed the Software in your own products and distribute it inside them in object form; and to practice the Reserved Claims as embodied in the Software and in conforming implementations. Your own code stays yours and carries no share-alike obligation. Improvements to the Software itself that you distribute to others must be under GGL-C-1.0 or GGL-OS-1.0.

**C.4 Startup Tier and evaluation.** A small business that, together with all its Affiliates, had fewer than {{{{SMALL_BIZ_MAX_WORKERS}}}} workers and less than {{{{SMALL_BIZ_MAX_REVENUE_USD}}}} USD in gross revenue last tax year, adjusted each year for US inflation (CPI-U) from {{{{INFLATION_BASE_YEAR}}}}, pays no fee. Every other term of GGL-C-1.0 applies to it. Anyone else may evaluate the Covered Works free for {{{{EVAL_DAYS}}}} days.

{fees}

{host}

{rep}

{fair}

{auth}

**C.10 Where the fees go.** Fees fund the maintenance of the Covered Works, the {{{{PROGRAM_NAME}}}} infrastructure, and the royalty pool in E.7. The Licensor publishes the pool calculation and payouts each year."""

def build(v):
    spdx = VARIANTS[v][0]
    body = "\n\n---\n\n".join([common_head(v), B("I.md"), B("S.md"), PART[v], patents(), enrichment(), B("M.md"), general()])
    body = body.replace("*Greater Good License 1.0. Licensor:", f"*{spdx}. Licensor:")
    body = body.replace("any later version of this license", "any later version of any license in the family")
    assert "$" not in body and "Part W" not in body and " W." not in body, [l for l in body.splitlines() if "Part W" in l or " W." in l][:3]
    return "\n" + body + "\n"

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "templates"), exist_ok=True)
    for v in VARIANTS:
        open(os.path.join(HERE, "templates", f"{VARIANTS[v][0]}.body"), "w", encoding="utf-8").write(build(v))
        print("built", VARIANTS[v][0])
