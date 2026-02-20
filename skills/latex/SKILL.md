---
name: latex
description: "LaTeX document compilation and management. When Claude needs to compile LaTeX documents (.tex files) for papers, presentations, or other academic content."
allowed-tools: Bash(latexmk*), Bash(xelatex*), Bash(pdflatex*), Bash(biber*), Bash(bibtex*), Bash(mkdir*), Bash(ls*), Read, Write, Edit
argument-hint: [tex-file-path]
---

# LaTeX Document Compilation

## Critical Rules

1. **Build artifacts go to `out/`, but the PDF stays in the source directory.** Before compiling, check for `.latexmkrc` — if missing, create one with the standard config (see Output Directory section). The `.latexmkrc` uses a Perl `END {}` block to copy the PDF back to the source directory after each build.
2. **NEVER write BibTeX entries from memory.** Always verify against web sources (CrossRef, Google Scholar, DOI lookup) before writing. See the `literature` skill.
3. **Check document class before adding packages.** Some classes load packages internally (e.g., `elsarticle` loads `natbib` — adding `\usepackage{natbib}` causes errors).

## Overleaf-Synced Projects

When a project is synced to Overleaf (via Dropbox or Git):
- The `out/` directory will sync to Overleaf but Overleaf ignores it — this is fine
- Always use `.latexmkrc` to enforce `out/` — Overleaf ignores this file too
- Overleaf compiles independently on its server; local compilation is for verification only
- The `.bst` file (e.g., `elsarticle-harv.bst`) lives in the source directory, not `out/`

## When NOT to Use

- Markdown documents — use plain markdown, not LaTeX
- Quick notes or drafts — LaTeX overhead not worth it
- Documents that don't need citations, equations, or precise formatting

## Local-Only Projects (No Overleaf)

Not all projects sync to Overleaf. For local-only projects:
- The same `out/` and `.latexmkrc` conventions apply — this keeps the working directory clean regardless of sync method
- There is no `paper/` symlink — `.tex` files live directly in the project root or a subdirectory
- Use `/latex-autofix` for compilation — it handles `.latexmkrc` creation if missing

## Templates

### Working Paper Template

When creating a **new working paper**, use the template. The canonical location is the Overleaf copy, with a local fallback:

1. `~/Library/CloudStorage/YOUR-CLOUD/Apps/Overleaf/Template/` (Overleaf source)
2. `~/Library/CloudStorage/YOUR-CLOUD/Task Management/templates/latex-wp/` (local copy)

The template contains:

| File | Purpose |
|------|---------|
| `main.tex` | Document entry point with structure |
| `your-template.sty` | Packages, layout, formatting, math environments |
| `your-bib-template.sty` | Bibliography config (biblatex, Paperpile cleanup, Harvard style) |
| `paperpile.bib` | Bibliography file (initially empty) |
| `out/` | Compilation output directory |

**To create a new working paper:**

1. Copy the template files to your new project folder
2. Rename as needed
3. Update `main.tex` with your title, author, abstract
4. Add references to `paperpile.bib`
5. Compile with `latexmk main.tex`

### Citation Style Toggle

The template uses **biblatex/biber** with a toggle for Harvard vs generic authoryear style.

In `main.tex`, control the style via package option:

```latex
\usepackage[harvard]{your-bib-template}    % Harvard style (default)
\usepackage[noharvard]{your-bib-template}  % Generic authoryear style
```

**Harvard style features:**
- Author names: Family, G.
- Volume in bold, issue in parentheses
- DOI/URL shown as "Available at: ..."
- No dashes for repeated authors

### Bibliography File Naming

**Always name the bibliography file `paperpile.bib`** — for any paper, whether using the working paper template or not. This is the standard naming convention across all projects (Paperpile exports use this name).

### Bibliography Commands

The template uses biblatex. In `main.tex`:

```latex
\printbibliography  % (not \bibliography{paperpile})
```

If you need natbib instead, do not load `your-bib-template` and use:
```latex
\bibliographystyle{agsm}
\bibliography{paperpile}
```

**Note:** This template is for working papers only. Other document types (presentations, theses, etc.) may require different templates.

---

## Output Directory

All LaTeX build artifacts (`.aux`, `.log`, `.bbl`, `.fls`, etc.) go to an `out/` subfolder relative to the source file. The **PDF is copied back** to the source directory after each successful build, so it lives alongside the `.tex` file for easy access. This keeps the working directory clean while keeping the deliverable visible.

## Configuration

The PDF-copy convention is enforced in **two places** — keep them in sync when making changes:

1. **`.latexmkrc`** (per-project) — Perl `END {}` block copies PDF after terminal/Claude Code builds
2. **VS Code settings** (`~/Library/Application Support/Code/User/settings.json`) — `copyPDF` tool in LaTeX Workshop recipes copies PDF after VS Code builds

Place a `.latexmkrc` in the project root to enforce output directory automatically.

### Auto-detecting Engine

This config automatically uses XeLaTeX if the document or any `\input{}`/`\include{}` file contains `\usepackage{fontspec}`, otherwise falls back to pdfLaTeX:

```perl
# .latexmkrc
$out_dir = 'out';

# Copy PDF back to source directory after build
END { system("cp $out_dir/*.pdf . 2>/dev/null") if defined $out_dir; }

# Recursively check for fontspec in main file and all \input{}/\include{} files
sub needs_xelatex {
    my ($file, $seen) = @_;
    $seen //= {};
    
    # Normalize and check if already visited
    return 0 if $seen->{$file};
    $seen->{$file} = 1;
    
    # Try with and without .tex extension
    my $filepath = -e $file ? $file : -e "$file.tex" ? "$file.tex" : undef;
    return 0 unless $filepath;
    
    open(my $fh, '<', $filepath) or return 0;
    my $dir = $filepath =~ s|/[^/]*$||r;  # Directory of current file
    $dir = '.' if $dir eq $filepath;
    
    while (<$fh>) {
        return 1 if /\\usepackage.*\{fontspec\}/;
        
        # Recurse into \input{} and \include{} files
        if (/\\(?:input|include)\{([^}]+)\}/) {
            my $subfile = $1;
            $subfile = "$dir/$subfile" unless $subfile =~ m|^/|;
            return 1 if needs_xelatex($subfile, $seen);
        }
    }
    close($fh);
    return 0;
}

# Auto-detect engine
$pdf_mode = 1;  # Default to pdflatex
foreach my $file (@ARGV) {
    if (needs_xelatex($file)) {
        $pdf_mode = 5;  # Switch to xelatex
        last;
    }
}

$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
```

### Manual Override

If auto-detection doesn't suit a project, use one of these explicit configs:

**pdfLaTeX** (standard LaTeX fonts):
```perl
# .latexmkrc
$out_dir = 'out';
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
END { system("cp $out_dir/*.pdf . 2>/dev/null") if defined $out_dir; }
```

**XeLaTeX** (system fonts, Unicode, OpenType features):
```perl
# .latexmkrc
$out_dir = 'out';
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
END { system("cp $out_dir/*.pdf . 2>/dev/null") if defined $out_dir; }
```

### Running

With any config:

```bash
latexmk document.tex
```

## Reference Checking

Every compilation must verify that all references resolve correctly. After compilation, check the log and report any issues found.

### Reference Check Script

After running latexmk, check for issues and display them as warnings:

```bash
# Compile
latexmk document.tex

# Check for reference issues and report exact problems
LOGFILE="out/document.log"
ISSUES=$(grep -E "(Reference.*undefined|Citation.*undefined|multiply defined)" "$LOGFILE" 2>/dev/null)

if [ -n "$ISSUES" ]; then
    echo ""
    echo "⚠️  REFERENCE ISSUES DETECTED:"
    echo "================================"
    echo "$ISSUES" | while read -r line; do
        echo "  • $line"
    done
    echo "================================"
    echo ""
fi
```

### What to Check For

| Pattern | Meaning |
|---------|---------|
| `Reference .* undefined` | `\ref{}` or `\autoref{}` pointing to non-existent label |
| `Citation .* undefined` | `\cite{}` referencing missing BibTeX entry |
| `Label .* multiply defined` | Same `\label{}` used more than once |

### Manual Compilation (if not using latexmk)

For biblatex (default in working paper template):
```bash
mkdir -p out
xelatex -output-directory=out document.tex
biber out/document
xelatex -output-directory=out document.tex
xelatex -output-directory=out document.tex
cp out/document.pdf ./document.pdf
```

For natbib (if using that instead):
```bash
mkdir -p out
pdflatex -output-directory=out document.tex
bibtex out/document
pdflatex -output-directory=out document.tex
pdflatex -output-directory=out document.tex
cp out/document.pdf ./document.pdf
```
