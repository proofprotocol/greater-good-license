## M. Contribution Markers

This section says how a Licensor marks any part of a Covered Work as contributed to a named organization, and makes everything not so marked uncontributed.

**M.1 Default: nothing is contributed.** No part of a Covered Work is contributed to any organization, standards body, consortium, foundation, project, or working group, except text, code, schemas, or other material that lies between Contribution Markers under M.2 and is listed in the Contribution Schedule under M.4. This holds whatever any other document, submission, pull request, email, meeting, membership agreement, charter, intellectual property policy, or contributor license says, including any term under which material submitted to a project is deemed contributed unless the submitter states otherwise. This section is that statement.

**M.2 Markers.** A contribution is marked by a start marker and an end marker, each on its own line, in exactly this form:

```
[CONTRIBUTED TO <orgname>]
...
[/END OF CONTRIBUTED TO <orgname>]
```

`<orgname>` is the organization's legal or registered name, written identically in both markers, case and spacing included. In source code, configuration, or any format where a bare line would break the file, each marker is placed alone inside a line comment of that format (for example `# [CONTRIBUTED TO <orgname>]`, `// [CONTRIBUTED TO <orgname>]`, or `<!-- [CONTRIBUTED TO <orgname>] -->`). Only the bracketed text is the marker; the comment syntax around it is not. In prose and documentation (Markdown, plain text) the bare form is used, so that a reader sees the marker in the rendered text; markers MUST NOT be hidden in a comment where the format displays bare lines.

**M.2a Formats without markers.** Some formats cannot carry markers reliably. In JSON, which has no comments, a contribution is declared only in the Contribution Schedule, by file path and JSON Pointer (RFC 6901) to each contributed element; the element at the pointer, with everything beneath it, is the contributed material. In YAML, markers MAY be placed in `#` comments, but YAML parsers discard comments when files are loaded and rewritten, so the Contribution Schedule entry is the authority: a YAML contribution MUST also be listed in the Schedule by file path and, where only part of the file is contributed, by the path to each contributed node. Where markers and the Schedule disagree for any format, the narrower of the two applies.

**M.3 Scope.** Everything strictly between a start marker and its matching end marker is contributed to the named organization, and to no other, on the terms the Contribution Schedule records for it. Everything outside every matched pair remains licensed under this license alone.

**M.4 Contribution Schedule.** Every contribution MUST appear in the Covered Work's Contribution Schedule, published in two forms that agree: `CONTRIBUTIONS.md` for people and `contributions.json` for machines. Each entry states the organization; the Covered Work and version; the scope, as a list of files each marked `by: markers` or `by: pointer` with the pointer or node path (M.2a); the terms of the contribution (a license name, or the identifier of a signed agreement); any Patent Schedule claims Contributed with it (Part P), by identifier, or none; the date; and the Licensor's signature. Markers naming an organization with no Schedule entry, and material in a file the Schedule entry does not list, contribute nothing. The Contribution Schedule is the companion of the Patent Schedule (Part P): the Patent Schedule says which claims are contributed, the Contribution Schedule says which text, code, and data are contributed and to whom.

**M.5 Fail closed.** A start marker without a matching end marker, an end marker without a matching start marker, markers whose organization names differ, or markers for the same organization nested inside one another, contribute nothing anywhere in the file in which they occur. Blocks for different organizations MAY nest; the inner material is then contributed to each named organization on its own Schedule terms. Blocks MUST NOT cross: a block that ends inside another block it did not start in contributes nothing.

**M.6 Who may mark.** Only the Licensor may place Contribution Markers in a Covered Work. The owner of a Recognized Lineage Node (Section E) may place them only around material within that node's own scope. Markers placed by anyone else contribute nothing.

**M.7 What a contribution does not change.** A contribution never removes or alters Section I (Original Inventor), the Inventor Line, the attribution required by Part S, or the Enrichment Lines of Section E; the contributed material carries them into the organization's work. A contribution of text or code grants no patent license unless the Schedule entry lists the Contributed claims (Part P).

**M.8 Per version.** A contribution attaches to the version of the Covered Work in which the markers appear. Removing or moving markers in a later version does not withdraw a contribution already made for an earlier version, and adding markers in a later version does not contribute the same material in earlier versions.

**M.9 Humans and machines.** Markers are plain text so that a person can see them and a machine can find them. The Licensor publishes a tool that, for any file and organization, lists the marked blocks, rejects any file in which M.5 makes the markers void, and produces a Contribution Extract containing only the contributed blocks or elements with the source file's SHA-256, the version, and the Schedule entry, so that anyone can verify that an extract matches the published source. A person reading the file and the tool reading the file MUST reach the same answer about what is contributed.
