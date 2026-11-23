"""Count keyword matches in the full texts of the reports (aid for manual coding).

The scripts never assigned a code: every match was a candidate passage that a reviewer read in context.
Full texts are not distributed with this repository (publisher copyright). To rerun the search,
convert your own copies of the PDFs to plain text (e.g., `pdftotext -layout ART13_SCP.pdf`) and name
each file <Study ID>.txt.

Usage:  python keyword_flags.py <folder with .txt files> [output.csv] [--snippets]
Output: one row per report with the number of matches of every term list in keyword_terms.json.
        With --snippets, the first matching passage of each list is added.
Only the Python standard library is required.
"""
import csv, json, re, sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    sys.exit(__doc__)
folder = Path(args[0])
out = Path(args[1]) if len(args) > 1 else Path("keyword_flags.csv")
snippets = "--snippets" in sys.argv

terms = json.load(open(Path(__file__).resolve().parent / "keyword_terms.json", encoding="utf-8"))
patterns = {f"{p.split('_')[0]}.{name}": re.compile(rx, re.I) for p, group in terms.items() for name, rx in group.items()}

# The search is limited to the text before the reference list.
REF = re.compile(r"^\s*(\d+\.?\s*)?(references|referencias|bibliography|bibliografía|bibliografia|referências|"
                 r"referencias bibliográficas|literatura citada|works cited)\s*$", re.I | re.M)

def body(text):
    heads = [m for m in REF.finditer(text) if m.start() > 0.35 * len(text)]
    return re.sub(r"\s+", " ", text[:heads[-1].start()] if heads else text)

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["study_id", "characters_searched"] + list(patterns) + ([f"{k}__passage" for k in patterns] if snippets else []))
    files = sorted(folder.glob("*.txt"))
    for path in files:
        b = body(path.read_text(encoding="utf-8", errors="ignore"))
        hits = {k: list(rx.finditer(b)) for k, rx in patterns.items()}
        row = [path.stem, len(b)] + [len(h) for h in hits.values()]
        if snippets:
            row += [b[max(0, h[0].start() - 140):h[0].end() + 140] if h else "" for h in hits.values()]
        w.writerow(row)
print(f"{len(files)} reports -> {out}")
