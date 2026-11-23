"""Draw the three figures of the review.

Usage:  python make_figures.py
Reads   ../04_Coded_Dataset/coded_dataset.csv and ../03_Study_Selection/prisma_flow.csv
Writes  figures/fig1_prisma.png, figures/fig2_year_country.png, figures/fig3_practices_period.png (600 dpi)
Requires matplotlib and numpy.
"""
import csv
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
FIG = HERE / 'figures'; FIG.mkdir(exist_ok=True)
G = list(csv.DictReader(open(HERE.parent / '04_Coded_Dataset' / 'coded_dataset.csv', encoding='utf-8-sig')))
for r in G:
    r['mets'] = {m.strip() for m in r['Metrics reported'].split(',')}
    r['periodo'] = '2020-2022' if int(r['Year']) <= 2022 else '2023-2026'
N = {r['stage'].strip(): int(r['n']) for r in csv.DictReader(open(HERE.parent / '03_Study_Selection' / 'prisma_flow.csv', encoding='utf-8'))}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})

# ---------------------------------------------------------------- Figure 1: PRISMA 2020
fig, ax = plt.subplots(figsize=(7.4, 8.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
def box(x, y, w, h, text, fc='white', bold=False, fs=8.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.25,rounding_size=0.8', fc=fc, ec='#333333', lw=0.9))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', linespacing=1.35)
def arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color='#333333', lw=0.9, shrinkA=0, shrinkB=0))
def side(y0, y1, label):
    ax.add_patch(FancyBboxPatch((0.5, y0), 5, y1 - y0, boxstyle='round,pad=0.2,rounding_size=0.8', fc='#D9E2F3', ec='#333333', lw=0.9))
    ax.text(3, (y0 + y1) / 2, label, rotation=90, ha='center', va='center', fontsize=8.6, fontweight='bold')
LX, LW, RX, RW = 9, 40, 56, 43
side(81, 97, 'Identification'); side(33, 77, 'Screening'); side(3, 29, 'Included')
box(LX, 81, LW, 16, f"Records identified (n = {N['Records identified']:,}):\nScopus (n = {N['Scopus']})\nWeb of Science (n = {N['Web of Science']})\nACM Digital Library (n = {N['ACM Digital Library']})\nIEEE Xplore (n = {N['IEEE Xplore']})")
box(RX, 84, RW, 10, f"Records removed before screening:\nDuplicate records (n = {N['Duplicate records removed']})")
box(LX, 67, LW, 8, f"Records screened\n(n = {N['Records screened (title and abstract)']})"); box(RX, 67, RW, 8, f"Records excluded\n(n = {N['Records excluded']})")
box(LX, 53, LW, 8, f"Reports sought for retrieval\n(n = {N['Reports sought for retrieval']})"); box(RX, 53, RW, 8, f"Reports not retrieved\n(n = {N['Reports not retrieved']})")
box(LX, 33, LW, 14, f"Reports assessed for eligibility\n(n = {N['Reports assessed for eligibility']})")
REASONS = ['Not focused on dropout prediction', 'Not undergraduate higher education', 'Data from outside Latin America', 'Review article', 'Published before 2020', 'Duplicate report', 'No performance metrics reported', 'Retracted']
box(RX, 28.5, RW, 23, f"Reports excluded (n = {N['Reports excluded']}):\n" + '\n'.join(f"{k.replace(' reported', '')} (n = {N[k]})" for k in REASONS), fs=7.6)
box(LX, 10, LW, 12, f"Studies included in the review\n(n = {N['Studies included in the review']})", fc='#E2EFDA', bold=True)
arrow(LX + LW / 2, 81, LX + LW / 2, 75); arrow(LX + LW / 2, 67, LX + LW / 2, 61); arrow(LX + LW / 2, 53, LX + LW / 2, 47); arrow(LX + LW / 2, 33, LX + LW / 2, 22)
arrow(LX + LW, 89, RX, 89); arrow(LX + LW, 71, RX, 71); arrow(LX + LW, 57, RX, 57); arrow(LX + LW, 40, RX, 40)
fig.savefig(FIG / 'fig1_prisma.png', dpi=600, bbox_inches='tight', facecolor='white'); plt.close(fig)

# ---------------------------------------------------------------- Figure 2: year and country
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={'width_ratios': [1, 1.25]})
yc = Counter(int(r['Year']) for r in G); years = sorted(yc)
b = a1.bar(years, [yc[y] for y in years], color='#4472C4', width=0.65)
a1.bar_label(b, fontsize=8); a1.set_ylabel('Number of studies'); a1.set_title('(a) Publication year', fontsize=9.5, loc='left')
a1.set_ylim(0, max(yc.values()) + 4)
cc = Counter(r['Country of the dataset'] for r in G); order = [c for c, _ in cc.most_common() if c != 'Multi-country'] + ['Multi-country']
order = order[::-1]
b = a2.barh(order, [cc[c] for c in order], color='#4472C4', height=0.65)
a2.bar_label(b, fontsize=8, padding=2); a2.set_xlabel('Number of studies'); a2.set_title('(b) Country of the dataset', fontsize=9.5, loc='left'); a2.set_xlim(0, max(cc.values()) + 3)
for a in (a1, a2):
    a.spines[['top', 'right']].set_visible(False); a.tick_params(labelsize=8)
fig.tight_layout(); fig.savefig(FIG / 'fig2_year_country.png', dpi=600, bbox_inches='tight', facecolor='white'); plt.close(fig)

# ---------------------------------------------------------------- Figure 3: reporting practices by period
P = [('Accuracy', lambda r: 'Accuracy' in r['mets']), ('Recall', lambda r: 'Recall' in r['mets']), ('F1-score', lambda r: 'F1' in r['mets']),
     ('AUC-ROC', lambda r: 'AUC-ROC' in r['mets']), ('Imbalance treatment', lambda r: r['Class imbalance treatment'] != 'None reported'), ('Multi-source data', lambda r: r['Data source'] == 'Multiple sources'),
     ('Ethics approval or exemption', lambda r: r['Ethics review'] != 'Not reported'), ('SHAP or LIME', lambda r: r['Explanation method'] in ('SHAP', 'LIME')), ('Public data', lambda r: r['Data availability'] == 'Public'),
     ('Temporal validation', lambda r: r['Validation strategy'] == 'Temporal'), ('Calibration', lambda r: r['Probability calibration'] == 'Yes')]
A = [r for r in G if r['periodo'] == '2020-2022']; B = [r for r in G if r['periodo'] == '2023-2026']
fig, ax = plt.subplots(figsize=(7.4, 3.9))
y = np.arange(len(P))[::-1]; h = 0.38
va = [100 * sum(f(r) for r in A) / len(A) for _, f in P]; vb = [100 * sum(f(r) for r in B) / len(B) for _, f in P]
b1 = ax.barh(y + h / 2, va, h, color='#A5A5A5', label=f'2020–2022 (n = {len(A)})'); b2 = ax.barh(y - h / 2, vb, h, color='#4472C4', label=f'2023–2025 (n = {len(B)})')
ax.bar_label(b1, fmt='%.0f', fontsize=7.5, padding=2); ax.bar_label(b2, fmt='%.0f', fontsize=7.5, padding=2)
ax.set_yticks(y); ax.set_yticklabels([p for p, _ in P], fontsize=8.5); ax.set_xlabel('Studies reporting the practice (%)'); ax.set_xlim(0, 108)
ax.spines[['top', 'right']].set_visible(False); ax.legend(frameon=False, fontsize=8.5, loc='lower right')
fig.tight_layout(); fig.savefig(FIG / 'fig3_practices_period.png', dpi=600, bbox_inches='tight', facecolor='white'); plt.close(fig)
print('figures written to', FIG)
