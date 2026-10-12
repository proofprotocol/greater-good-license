## E. Enrichment and Lineage

A Covered Work can grow. Section E lets other inventors enrich it, be named for what they add, and choose how their own portion is used, without ever changing what sits above them.

**E.1 Enrichment.** Anyone may enrich a Covered Work by adding something separable that builds on it: a method, an improvement, a profile, a test suite, or text. Each enrichment is recorded as a Lineage Node.

**E.2 Lineage Node.** A Lineage Node is a record that states: its parent nodes, by hash; the contributor's name and ORCID; the Covered Work and version it builds on; the scope of the contribution, by section, claim, and description; the SHA-256 hash of the contributed material; the contributor's terms under E.5; whether it touches a root claim (E.8); and the DOI of the node's deposit on Zenodo under the contributor's ORCID. A node's hash is the SHA-256 of its record in canonical JSON (RFC 8785), excluding the hash itself. The root node is the Inventor Record (Section I). Because every node names its parents by hash, the nodes form a hash-linked tree in which any change to any node breaks every hash below it.

**E.3 Recognition.** A node is Recognized when the contributor of each of its parent nodes has countersigned a Recognition record naming the node's hash, deposited with a DOI. A node that is not Recognized is a Fork. A Fork may be used under the terms of the nodes above it, must be labeled as a fork wherever it is named, and receives no pool share under E.7.

**E.4 Scope, and no override.** A node's terms govern only the contributor's own portion, as its scope describes. Everything a node inherits stays under the terms of the nodes above it, up to the root. No node may relax, remove, replace, or add conditions to the terms of any node above it, including Section I and the Inventor Line.

**E.5 Node terms.** Each contributor chooses one term for their portion:

- **Contributed:** free for any use, including commercial use, and royalty-free under any patent claim the contributor holds on that portion;
- **Inherit:** the same terms as its parent node; or
- **Reserved:** available on the contributor's own published price, for that portion only.

A contributor may also require their Enrichment Line (E.6) in attribution.

**E.6 Obligations stack.** Anyone using a work at a node must meet the terms of the root and of every node above it, and must carry the Inventor Line and the Enrichment Line of each Recognized node above it:

```
Enriched by: <name> (ORCID <orcid>), lineage node <first 12 hex of node hash>, Record DOI <doi>
```

No one other than the root's inventor may be named original inventor (I.4). Contributors are named as enrichers of what they added.

**E.7 Royalty pool.** A licensee pays the Part W fee once, however deep the tree. The Licensor pays each Recognized node whose terms are Contributed or Inherit the pool share that node declared, out of fees collected on works whose ancestry includes that node. In the ancestry of any node, the pool shares together must not exceed {{POOL_CAP_PCT}}% of the fee. A Reserved node charges its own price and takes no pool share; a node takes one or the other, never both. The Licensor publishes the pool calculation and payouts each year.

**E.8 Root claims and inventorship.** A Lineage Node must state whether its contribution touches any claim of the root's patents or patent applications. A node that does is Recognized only if its contributor has assigned to the Licensor their interest in each touched root claim, by a recorded assignment cited in the node. Inventorship is decided by patent law, not by this license. E.8 decides recognition and pool eligibility.

**E.9 The lineage file.** The Licensor keeps the canonical lineage of each Covered Work at {{LINEAGE_URL}}. Anyone may check every hash, parent link, recognition, scope, term, assignment, and pool limit in it with the published verifier.