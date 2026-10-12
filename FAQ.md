# Greater Good License 1.0: FAQ

Short answers. The license texts control; where this FAQ and a license differ, the license wins.

## The basics

**What is the Greater Good License?**
A family of three licenses that share one core. GGL-OS (open source), GGL-EGR (education, government, research), and GGL-C (commercial). All three share the same sections on the Original Inventor (I), specification text (S), patents (P), enrichment and lineage (E), contribution markers (M), and general terms (G), word for word. Each adds one part of its own: O, R, or C.

**Which one applies to me?**
- You release your own software as open source under share-alike terms: GGL-OS. Free.
- You are a school, government body, research institution, nonprofit, or an individual learning: GGL-EGR. Free, non-commercial.
- You are a small business under the Startup Tier limits: GGL-C, fee waived.
- You are evaluating: GGL-C evaluation period, free.
- Everyone else using it commercially: GGL-C, with a fee.

A Covered Work's LICENSE.md says which of the three it is offered under.

**Can I read, cite, copy, and share the specifications for free?**
Yes, always, under every license. Specification text is under Part S (CC BY-ND 4.0 for Proof Protocol specs): copy and share it verbatim with attribution.

## Fees

**How can a license "for the greater good" have a fee section?**
Because nothing is free. Someone pays for the work, and the question is who and on what terms. The GGL answers that in the open:

1. **Free where it does the most good.** Open source projects, schools, governments, researchers, nonprofits, individuals, and small businesses pay nothing. The fee falls only on commercial users above the Startup Tier, the organizations that profit from the work.
2. **Free until profit.** A company starts paying when it is big enough to have the revenue, not before. The fee is a give-back out of what the work helps earn, not a gate in front of it.
3. **Paid by the user, not by the measured.** A specification that measures security controls is worthless if the Providers it measures pay to shape it. Fees from many licensees, at the same published rate for everyone (C.8), keep the work independent of any one sponsor. Paying a fee buys use, never influence: no licensee gains any say over the specification, its outcomes, or any Registry, Issuer, or Witness decision (Proof Economy Code of Ethics, Ethical Capital Principle).
4. **The money is accounted for.** Fees fund maintenance of the Covered Works, the infrastructure, and the royalty pool that pays later contributors (C.10, E.7). The pool calculation and payouts are published every year.
5. **Same price for everyone.** Published rates, paid by at least one unaffiliated customer, are fair, reasonable, and nondiscriminatory by definition (C.8). No secret deals.

"Greater good" means the work spreads as widely as possible and stays honest. A license that gives everything away to everyone, including the largest companies, usually ends with the work abandoned or captured by whoever funds it. The fee is what keeps it alive and independent.

**What are the rates?**
Published at the rates URL in each Covered Work's GGL-C parameters, the same for every licensee.

**Is GGL-C open source?**
No. GGL-C is a source-available commercial license. GGL-OS is the open source member of the family. Being clear about that is the point of having three.

## Patents

**Does the license give me a patent license?**
Only for claims listed in the Covered Work's Patent Schedule (Part P). Claims not listed there are Reserved. For a Reserved claim, contact the licensing address in LICENSE.md.

**What does "contributed" mean?**
Nothing in a Covered Work is contributed to any organization, standards body, consortium, foundation, or working group unless it sits between `[CONTRIBUTED TO <orgname>]` and `[/END OF CONTRIBUTED TO <orgname>]` markers and is listed in a signed Contribution Schedule (Section M). Everything else stays with the Licensor.

**Can a contribution be taken back?**
No. Once the Contribution Schedule is signed, the contribution of the marked material to that organization is permanent. That is what makes it safe for the organization to accept.

## Inventors and contributors

**Who is the Original Inventor, and why can't that change?**
Craig Thomas Ellrod (ORCID 0009-0004-1058-7666), established by an Inventor Record deposited on Zenodo with a DOI. Section I makes that identification permanent: it travels with every copy, derivative, implementation description, and conformance claim. Inventorship of any patent is still decided by patent law; Section I is about attribution.

**Can I build on a Covered Work and be credited or paid?**
Yes. Section E lets anyone add a separable enrichment, recorded as a Lineage Node: a hash-linked record with your ORCID and a Zenodo DOI. Once Recognized by the nodes above it, your node chooses its own terms for your portion and can take a share of the royalty pool. Your terms cover only your portion; you can never change the terms of anything above you.

## Status and tooling

**Why do the licenses say DRAFT?**
Until the Inventor Record DOI and the commercial rate values are published, every rendered license is marked DRAFT and grants nothing beyond reading, citing, and discussing the work. The marking is removed when those values are set.

**Can a machine check a license?**
Yes. `python3 ggl.py check` validates a parameter file, `render` refuses to produce a license until every value passes, and `verify` fails on any edit to the canonical text. A person and a program reach the same result.
