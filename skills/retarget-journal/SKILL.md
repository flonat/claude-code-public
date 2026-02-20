---
name: retarget-journal
description: "Retarget a paper to a different journal. Renames folders, swaps bib files, updates citation keys, reformats to target requirements, and compiles to verify."
allowed-tools: Bash(latexmk*), Bash(pdflatex*), Bash(xelatex*), Bash(mkdir*), Bash(ls*), Bash(cp*), Bash(mv*), Bash(git*), Read, Write, Edit, Glob, Grep, Task
argument-hint: [target-journal-name]
---

# Retarget Journal Skill

> Switch a paper manuscript from one journal to another. Handles folder renaming, bibliography swaps, citation key updates, formatting changes, and compilation verification.

## When to Use

- Switching a paper's target venue (e.g., Journal A to Journal B, Journal C to Journal D)
- After a rejection when resubmitting to a different journal
- When strategic decisions change the target venue mid-drafting

## Before Starting

Ask the user for:

1. **Current project path** — where is the paper?
2. **Target journal** — full name and abbreviation
3. **What changes?** — some retargets are minor (formatting), others are major (restructuring)

Read the project's `CLAUDE.md` and `README.md` to understand current state.

---

## Workflow

### Phase 1: Assess Scope

Read the current manuscript and compare against the target journal's requirements:

| Check | What to compare |
|-------|----------------|
| **Word/page limit** | Does the draft fit? Need to cut or can expand? |
| **Required sections** | Does the target need sections the current draft lacks? (e.g., "Relevance Statement", "AI Disclosure") |
| **Citation style** | Author-year vs numbered? natbib vs biblatex? |
| **Formatting** | Template class? Column layout? Font requirements? |
| **Supplementary material** | Online appendix conventions? |

Present the assessment to the user before proceeding.

### Phase 2: Rename and Restructure

1. **Rename project folder** if it references the old journal:
   ```bash
   mv "old-journal-name/" "new-journal-name/"
   ```

2. **Update Overleaf symlink** if one exists:
   ```bash
   # Remove old symlink
   rm paper/
   # Create new symlink to the correct Overleaf directory
   ln -s "/path/to/Overleaf/new-project" paper
   ```

3. **Update folder references** in `CLAUDE.md`, `README.md`, `.gitignore`

### Phase 3: Bibliography

1. **Swap `.bib` file** if the user provides a new Paperpile export
2. **Update citation keys** across all `.tex` files:
   - Read the new `.bib` to get the new key format
   - Find all `\cite{...}`, `\citet{...}`, `\citep{...}`, `\citeauthor{...}` commands in `.tex` files
   - Map old keys to new keys (match by author + year)
   - Replace all occurrences
3. **Validate** — run `/validate-bib` to ensure no missing or unused keys

### Phase 4: Formatting

1. **Switch document class/template** if needed
2. **Add required sections** (e.g., data availability, AI disclosure, conflict of interest)
3. **Adjust page layout** (margins, columns, font size)
4. **Update `\bibliographystyle{}`** if citation style changes
5. **Update abstract** — check word limit for target journal

### Phase 5: Update Documentation

1. **Project `CLAUDE.md`** — update target journal, formatting notes
2. **Project `README.md`** — update journal reference, submission info
3. **`MEMORY.md`** — carry forward any learnings, update journal-specific notes
4. **Notion Research Pipeline** — update the Target Journal and Status fields

### Phase 6: Compile and Verify

1. Compile to `out/` with `latexmk`
2. Fix all warnings (overfull/underfull)
3. Check page count against target journal limit
4. Verify all citations resolve
5. Visual check: does the formatting look right for the target venue?

### Phase 7: Confirm

Report a summary:

```
Retargeted [Paper Name]: [Old Journal] → [New Journal]

Changes made:
- Folder: [old path] → [new path]
- Symlink: updated to [new Overleaf project]
- Bibliography: [N] citation keys updated
- Sections added: [list]
- Sections removed: [list]
- Page count: [N] pages (limit: [M])
- Compilation: clean (0 warnings)

Updated: CLAUDE.md, README.md, Notion
```

---

## Important Rules

- **Never delete the old `.bib` file** — rename it to `old-journal.bib.bak` as a safety copy
- **Verify citation key mappings** with the user before bulk-replacing — automated matching can misfire on common surnames
- **Don't restructure content** without approval — some retargets only need formatting changes, not rewriting
- **Preserve git history** — commit the retarget as a single, well-documented commit

---

## Cross-References

| Skill | When to use alongside |
|-------|----------------------|
| `/validate-bib` | After Phase 3 to verify all citation keys |
| `/latex-autofix` | **Default compiler** — use for compilation with auto error resolution |
| `/latex` | For manual compilation config and `.latexmkrc` setup |
| `/proofread` | After retarget to check for remnants of old journal formatting |
| `/sync-notion` | After Phase 5 to sync with central context library |
