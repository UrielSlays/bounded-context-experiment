"""Render the MBCX-01 presentation figures from data/mbcx01-record-2026-09-26.json.

Needs matplotlib, which the verifier and the suites do not (see requirements.txt beside
this file). Run from the repository root or from this directory:

    python -m pip install -r docs/presentation/requirements.txt
    python docs/presentation/make_figures.py

Writes SVG and PNG pairs into docs/presentation/figures/. Commit dates for the
suite-growth figure are read from this repository's git history at run time, so
the figure is reproducible from a clean checkout of the branch.
"""
from __future__ import annotations

import datetime as dt
import json
import textwrap
import math
import os
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(HERE, "data", "mbcx01-record-2026-09-26.json")
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1B2A49"
INK = "#22262E"
SLATE = "#5A6473"
MIST = "#B9C1CC"
FOG = "#E6E9EE"
PAPER = "#FFFFFF"
AMBER = "#D08C1E"
BRICK = "#8E3B3B"
CREAM = "#FBF7EF"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "<account>Vu Sans", "Arial"],
    "font.size": 9,
    "axes.edgecolor": SLATE,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.titleweight": "regular",
    "svg.fonttype": "none",
})
SERIF = {"fontfamily": ["Georgia", "<account>Vu Serif"]}
GLYPH = {"fontfamily": ["Segoe UI Symbol", "<account>Vu Sans"]}


def load():
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def git_date(sha: str) -> dt.datetime:
    out = subprocess.run(["git", "-C", REPO, "show", "-s", "--format=%cI", sha],
                         capture_output=True, text=True, check=True).stdout.strip()
    return dt.datetime.fromisoformat(out).astimezone(dt.timezone.utc)


def title(fig, text, sub=None):
    # Wrap both lines inside the canvas: at 12.4 in wide the 16 pt serif title
    # holds about 88 characters per line and the 9.5 pt subtitle about 165.
    tl = textwrap.wrap(text, 88)
    y = 0.955
    for line in tl:
        fig.text(0.04, y, line, fontsize=16, color=NAVY, **SERIF)
        y -= 0.034
    if sub:
        y -= 0.003
        for para in sub.split("\n"):
            for line in textwrap.wrap(para, 165):
                fig.text(0.04, y, line, fontsize=9.5, color=SLATE)
                y -= 0.024


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=220, facecolor=PAPER)
    plt.close(fig)
    print("wrote", name)


def box(ax, x, y, w, h, fc=PAPER, ec=NAVY, lw=1.2, r=0.12, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, ls=ls)
    ax.add_patch(p)
    return p


def arrow(ax, x0, y0, x1, y1, color=SLATE, lw=1.1, style="-|>"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, color=color,
                                 lw=lw, mutation_scale=10, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- figure 1
def fig1(d):
    p = d["prereg"]
    fig = plt.figure(figsize=(12.4, 7.2))
    title(fig, "The registered experiment, before a single model call",
          "What one run of MBCX-01 is: a frozen cohort, one pair per scenario, six call positions, one look. Every number is registered in the design of record.")
    ax = fig.add_axes([0.03, 0.05, 0.94, 0.83])
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")

    # --- panel 1: the cohort funnel
    box(ax, 0.2, 2.75, 3.1, 3.55, fc=CREAM, ec=MIST, lw=0.8)
    ax.text(0.4, 6.05, "1  The cohort is frozen first", fontsize=11, color=NAVY, **SERIF)
    levels = [(f"{p['generated_candidates']:,} candidates generated", 2.7, 5.25),
              (f"{p['n_pairs']} retained", 2.1, 4.45),
              (f"{p['motifs']} motifs x {p['per_motif']} scenarios", 2.5, 3.65)]
    for i, (lab, w, y) in enumerate(levels):
        cx = 1.75
        shade = [FOG, MIST, NAVY][i]
        tc = [INK, INK, PAPER][i]
        box(ax, cx - w / 2, y - 0.3, w, 0.6, fc=shade, ec=shade, r=0.08)
        ax.text(cx, y, lab, ha="center", va="center", fontsize=9, color=tc, fontweight="bold" if i == 2 else "normal")
        if i < 2:
            arrow(ax, cx, y - 0.32, cx, y - 0.48)
    ax.text(1.75, 3.05, "eligibility recomputed after one cut;\nsupplied eligibility booleans are discarded",
            ha="center", va="center", fontsize=7.6, color=SLATE, style="italic")

    # --- panel 2: one pair
    box(ax, 3.6, 2.75, 5.1, 3.55, fc=CREAM, ec=MIST, lw=0.8)
    ax.text(3.8, 6.05, "2  One pair per scenario: two conditions, six model calls", fontsize=11, color=NAVY, **SERIF)
    lanes = [("BC  bounded context", 5.15, "the candidate carrier picks the object set"),
             ("OM  oracle memory", 3.85, "the independent gold read-set picks it")]
    for lab, y, note in lanes:
        ax.text(3.85, y + 0.62, lab, fontsize=9, color=NAVY, fontweight="bold")
        ax.text(3.85, y + 0.40, note, fontsize=7.6, color=SLATE, style="italic")
        nodes = [("A0", True), ("B", True), ("writer", False), ("cold A1", True)]
        xs = [4.35, 5.45, 6.55, 7.85]
        for (name, is_model), x in zip(nodes, xs):
            if is_model:
                ax.add_patch(Circle((x, y), 0.27, fc=NAVY, ec=NAVY))
                ax.text(x, y, name, ha="center", va="center", fontsize=8, color=PAPER, fontweight="bold")
            else:
                box(ax, x - 0.42, y - 0.24, 0.84, 0.48, fc=PAPER, ec=SLATE, lw=1.0, r=0.06)
                ax.text(x, y, name, ha="center", va="center", fontsize=8, color=INK)
        for x0, x1 in zip(xs[:-1], xs[1:]):
            arrow(ax, x0 + 0.29, y, x1 - 0.30 if x1 != 6.55 else x1 - 0.44, y)
    ax.text(6.15, 3.12, "same scenario, cut, observation, action universe, schema, instructions and transport;\n"
                        "the two conditions differ only in how the object set is selected",
            ha="center", va="center", fontsize=7.6, color=SLATE, style="italic")
    ax.text(8.5, 4.5, "3 model nodes\nper condition,\n6 per pair", ha="right", va="center", fontsize=7.8, color=NAVY, fontweight="bold")

    # --- panel 3: totals
    box(ax, 9.0, 2.75, 3.2, 3.55, fc=NAVY, ec=NAVY, lw=0.8)
    ax.text(9.2, 6.05, "3  What one run adds up to", fontsize=11, color=PAPER, **SERIF)
    ax.text(10.6, 5.35, f"{p['scheduled_call_positions']:,}", ha="center", va="center", fontsize=26, color=PAPER, **SERIF)
    ax.text(10.6, 4.85, "scheduled model calls\n(768 pairs x 6 positions)", ha="center", va="center", fontsize=8, color=MIST)
    ax.text(10.6, 4.2, "one look at n = 768", ha="center", va="center", fontsize=10, color=PAPER, fontweight="bold")
    ax.text(10.6, 3.62, f"family error {p['family_error']:.2f}\nnoninferiority margin {p['noninferiority_margin']:+.2f}\nOM floor {p['om_floor']:.2f}",
            ha="center", va="center", fontsize=8, color=MIST)
    ax.text(10.6, 3.0, "no retries counted as calls;\nretries are capped separately", ha="center", va="center", fontsize=7.4, color=MIST, style="italic")

    # --- the decision rail
    ax.text(0.4, 2.3, "The registered decision order, and where it stands today", fontsize=11, color=NAVY, **SERIF)
    steps = [
        ("1", "Reconstruct the bundle\nfrom pinned git objects", "passed: exit 0,\n156 frozen tests", True),
        ("2", "No blocking council\ndefect", "passed: r13.2\n3 of 3 CONFIRMED", True),
        ("3", "Exactness, accounting,\nboundedness, affordability\nover 100 physical cells", "not run: carriers, grid runner,\nexactness runner unbuilt;\nharness built, no live run", False),
        ("4", f"Route gate: {p['route_trials']} trials,\nat most {p['route_max_failures']} failures,\nin an approved ceiling", f"not run: {p['route_scheduled_positions']:,} calls;\nno ceiling approved", False),
        ("5", "Owner authorizes\nthe paid run", "not asked", False),
        ("6", "Run once, publish every\nregistered result", "not run", False),
    ]
    x = 0.3
    w = 1.9
    for n, lab, state, done in steps:
        fc = NAVY if done else PAPER
        ec = NAVY if done else SLATE
        box(ax, x, 0.95, w, 1.05, fc=fc, ec=ec, lw=1.1, ls="-" if done else (0, (3, 2)))
        ax.text(x + 0.14, 1.86, n, fontsize=12, color=PAPER if done else NAVY, **SERIF)
        ax.text(x + 0.42, 1.5, lab, fontsize=7.6, color=PAPER if done else INK, va="center")
        ax.text(x + w / 2, 0.62, state, fontsize=7.4, color=NAVY if done else BRICK, ha="center", va="center",
                fontweight="bold" if done else "normal")
        if n != "6":
            arrow(ax, x + w + 0.02, 1.47, x + w + 0.13, 1.47, color=SLATE)
        x += w + 0.14
    ax.text(0.4, 0.12, "Solid = passed with zero provider calls. Dashed = not run. The design itself authorizes no provider call: the route gate at step 4 needs an owner-approved ceiling, and the run at step 6 needs his separate authorization at step 5.",
            fontsize=7.6, color=SLATE, style="italic")
    save(fig, "fig1-registered-experiment")


# ---------------------------------------------------------------- figure 2
VERDICT = {
    "GO": (NAVY, PAPER, "✓"),
    "GWF": (AMBER, INK, "~"),
    "NOGO": (BRICK, PAPER, "✕"),
    "GTC": (NAVY, PAPER, "▶"),
    "CD": (AMBER, INK, "↻"),
    None: (PAPER, SLATE, "·"),
}


def heat(ax, rounds, label, seat_labels=True):
    n = len(rounds)
    for j, r in enumerate(rounds):
        for i, seat in enumerate(("s1", "s2", "s3")):
            v = r.get(seat)
            fc, tc, g = VERDICT[v]
            ax.add_patch(Rectangle((j, 2 - i), 1, 1, fc=fc, ec=PAPER, lw=1.5))
            ax.text(j + 0.5, 2 - i + 0.5, g, ha="center", va="center", fontsize=10, color=tc, **GLYPH)
            if r.get(f"{seat}_seal_breached"):
                ax.add_patch(Rectangle((j + 0.08, 2 - i + 0.08), 0.84, 0.84, fc="none", ec=PAPER, lw=1.4, ls=(0, (2, 1.5))))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 3)
    ax.set_xticks([j + 0.5 for j in range(n)])
    ax.set_xticklabels([r["round"] for r in rounds], fontsize=8)
    ax.set_yticks([2.5, 1.5, 0.5])
    ax.set_yticklabels(["Claude seat", "ChatGPT seat", "Codex exec seat"] if seat_labels else ["", "", ""], fontsize=8)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(label, loc="left", fontsize=10.5, color=NAVY, pad=6, **SERIF)


def fig2(d):
    rounds = d["rounds"]
    arcs = [("design", "Design council: 15 rounds to a frozen instrument (11 to 14 August 2026)"),
            ("build", "Build acceptance council: 8 rounds on the production authorities (14 to 16 August)"),
            ("cohort_design", "Cohort content design: 3 rounds"),
            ("cohort_build", "Cohort build: 2 rounds")]
    fig = plt.figure(figsize=(12.4, 8.0))
    title(fig, "Every round, every seat, until three seats said the same thing",
          "Three reviewers per round, each sealed from the others until it answers (from round seven the two browser seats kept their own thread across rounds, by owner ruling; the seal is between seats). A round advances on evidence, never on a vote count.\nA dashed inner border marks a report whose seal between seats was breached; it counted as technical evidence, never as an independent vote.")
    gs = fig.add_gridspec(2, 3, left=0.09, right=0.98, top=0.815, bottom=0.18, hspace=1.0, wspace=0.12,
                          width_ratios=[8, 3, 2], height_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[1, 2])
    by = {a: [r for r in rounds if r["arc"] == a] for a, _ in arcs}
    heat(ax1, by["design"], arcs[0][1])
    heat(ax2, by["build"], arcs[1][1])
    heat(ax3, by["cohort_design"], arcs[2][1], seat_labels=False)
    heat(ax4, by["cohort_build"], arcs[3][1], seat_labels=False)

    # findings bar under the design heatmap
    pos = ax1.get_position()
    axb = fig.add_axes([pos.x0, pos.y0 - 0.125, pos.width, 0.075])
    xs = list(range(len(by["design"])))
    for j, r in enumerate(by["design"]):
        f = r.get("findings")
        if f is None:
            axb.text(j + 0.5, 1, "n/r", ha="center", va="bottom", fontsize=6.5, color=SLATE)
        else:
            axb.bar(j + 0.5, f, width=0.72, color=MIST, ec="none")
            fd = r.get("folded")
            if fd is not None:
                axb.bar(j + 0.5, fd, width=0.72, color=SLATE, ec="none")
            axb.text(j + 0.5, f + 0.8, str(f) if fd in (None, f) else f"{f} / {fd}", ha="center", va="bottom", fontsize=6.8, color=INK)
    axb.set_xlim(0, len(xs))
    axb.set_ylim(0, 30)
    axb.axis("off")
    fig.text(pos.x0, pos.y0 - 0.145, "findings listed in the round record (light) and adopted before the next round (dark); \"listed / adopted\" marks the rounds whose synthesis declined some items; n/r = not recorded",
             fontsize=7.6, color=SLATE, style="italic")
    r8 = next(r for r in by["design"] if r["round"] == "r8")
    fig.text(pos.x0, pos.y0 - 0.163, f"r8: no browser-seat verdict file is banked; the round is recorded in aggregate as {r8['aggregate']}",
             fontsize=7.6, color=SLATE, style="italic")

    # annotation: the premise correction on build r1-r3
    pc = d["premise_correction"]
    ax2.add_patch(Rectangle((0, 0), 3, 3, fc="none", ec=BRICK, lw=1.4, ls=(0, (3, 2))))
    fig.text(0.09, 0.115, f"Dashed box: build rounds 1 to 3 reviewed against a declared adversary that did not exist "
                          f"(an API caller on a system with no API). Cost: {pc['rounds_spent']} rounds, {pc['verdicts_spent']} verdicts and one capability report, "
                          f"and a wiring-freeze mechanism built for that phantom and then reverted. The owner caught it, in chat.",
             fontsize=7.8, color=INK, wrap=True)
    # legend
    lx = 0.05
    for k, lab in (("GO", "GO or CONFIRMED"), ("GWF", "GO with fixes"), ("NOGO", "NO-GO"),
                   ("GTC", "GO-TO-CODE"), ("CD", "CONTINUE-DESIGN"), (None, "no verdict banked")):
        fc, tc, g = VERDICT[k]
        fig.patches.append(Rectangle((lx, 0.045), 0.014, 0.024, transform=fig.transFigure, fc=fc, ec=SLATE if k is None else fc, lw=0.6))
        fig.text(lx + 0.007, 0.057, g, ha="center", va="center", fontsize=8, color=tc, **GLYPH)
        fig.text(lx + 0.02, 0.057, lab, va="center", fontsize=8, color=INK)
        lx += 0.135
    fig.patches.append(Rectangle((lx, 0.045), 0.014, 0.024, transform=fig.transFigure, fc=NAVY, ec=NAVY, lw=0.6))
    fig.patches.append(Rectangle((lx + 0.0015, 0.047), 0.011, 0.02, transform=fig.transFigure, fc="none", ec=PAPER, lw=1.0, ls=(0, (2, 1.5))))
    fig.text(lx + 0.02, 0.057, "seal breached: evidence only", va="center", fontsize=8, color=INK)
    save(fig, "fig2-council-verdicts")


# ---------------------------------------------------------------- figure 3
def fig3(d):
    s = d["suite"]
    cg = d["codex_cli_gate"]
    fig = plt.figure(figsize=(12.4, 7.4))
    title(fig, "The witness suite grew under review while the frozen code held",
          "Left: the witness names the build ledger carries at each commit, a historical count per point; the last point is the set the verifier runs today; written red before green, with the pins the record names as such. Right: what the codex edge gate found, round by round, until P2 alone remained.")
    ax = fig.add_axes([0.07, 0.14, 0.56, 0.68])
    pts = [(git_date(sha), rows, wit, lab) for sha, rows, wit, lab in s["build_series"]]
    pts.sort(key=lambda t: t[0])
    xs = [p[0] for p in pts]
    ys = [p[2] for p in pts]
    ax.step(xs, ys, where="post", color=NAVY, lw=2.2, label="witness names in the ledger at that commit")
    ax.scatter(xs, ys, s=16, color=NAVY, zorder=3)
    fz = [(git_date(sha), n, lab) for sha, n, lab in s["frozen_series"]]
    fz.sort(key=lambda t: t[0])
    fx = [p[0] for p in fz] + [xs[-1]]
    fy = [p[1] for p in fz] + [fz[-1][1]]
    ax.step(fx, fy, where="post", color=AMBER, lw=2.2, label="frozen r13.2 suite (design side)")
    ax.scatter(fx[:-1], fy[:-1], s=16, color=AMBER, zorder=3)
    ax.set_ylim(0, 320)
    ax.set_ylabel("witnesses named in the ledger at that commit")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M", tz=dt.timezone.utc))
    ax.grid(axis="y", color=FOG)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    # annotations
    marks = {"c2e011b": ("ETW consumer built", 12), "fd26275": ("wiring freeze reverted (95 to 94)", -34),
             "f35851e": ("cohort engine slice", -30), "d13ab7b": ("codex r9: 289", 10), "2fd3897": ("content-final: 76", 12)}
    for sha, rows, wit, lab in s["build_series"]:
        if sha in marks:
            txt, dy = marks[sha]
            x = git_date(sha)
            ax.annotate(txt, (x, wit), xytext=(0, dy), textcoords="offset points", fontsize=7.2, color=INK,
                        ha="left" if dy > 0 else "right", arrowprops=dict(arrowstyle="-", color=MIST, lw=0.8))
    ax.text(fx[0], 145 + 10, "145 frozen at r13.2; the frozen code changed in four declared commits\n(three ratified amendments and one acceptance fold), 145 to 156;\nthe frozen documents in one more, owner-ratified on 16 August", fontsize=7.2, color=AMBER, va="bottom")

    axr = fig.add_axes([0.70, 0.14, 0.27, 0.68])
    n = len(cg["rounds"])
    axr.bar(range(n), cg["p1"], color=BRICK, label="P1")
    axr.bar(range(n), cg["p2"], bottom=cg["p1"], color=MIST, label="P2")
    for i, t in enumerate(cg["total"]):
        axr.text(i, t + 0.25, str(t), ha="center", fontsize=8, color=INK)
    axr.set_xticks(range(n))
    axr.set_xticklabels(cg["rounds"], fontsize=8)
    axr.set_ylim(0, 12)
    axr.set_ylabel("findings per codex review round")
    axr.grid(axis="y", color=FOG)
    for sp in ("top", "right"):
        axr.spines[sp].set_visible(False)
    axr.legend(frameon=False, fontsize=8, loc="upper right")
    axr.text(0.02, 0.97, f"{sum(cg['total'])} findings over nine rounds;\n{sum(cg['total']) - 1} folded red-first, one r4 fix\nreverted in full; r9 returned P2 only.\nr10 was not run.",
             transform=axr.transAxes, fontsize=7.6, color=INK, va="top")
    save(fig, "fig3-suite-and-gate")


# ---------------------------------------------------------------- figure 4
def fig4(d):
    items = d["issues"]["items"]
    fam_order = ["smoke", "physical", "gates", "build", "r4", "r5", "keys", "design", "repo"]
    fam_label = {"smoke": "the smoke run", "physical": "physical stage", "gates": "review gates", "build": "build rounds 1 to 3",
                 "r4": "acceptance r4", "r5": "acceptance r5", "keys": "key material", "design": "design series", "repo": "repository"}
    state_fc = {"open": AMBER, "closed": NAVY, "void": FOG, "partial": MIST}
    counts = {k: sum(1 for it in items if it[2] == k) for k in ("closed", "void", "partial", "open")}
    gh = d["github_issues"]
    snap = d["issues"]["snapshot_date"]
    fig = plt.figure(figsize=(12.4, 6.6))
    title(fig, f"Where the arc stands: the committed tracker of {snap} beside the live tracker of {gh['as_of']}",
          f"Committed tracker: {len(items)} items: {counts['closed']} closed, {counts['void']} void or superseded, {counts['partial']} half closed, {counts['open']} open. Live tracker: {gh['filed']} issues: {gh['open']} open, {gh['closed']} closed. " "Left: the committed tracker file, one dot per item as it stood on its own date; an outer ring marks the items it calls load-bearing. Right: what the repository's issue tracker says stands between today and a paid run.")
    ax = fig.add_axes([0.05, 0.10, 0.62, 0.76])
    ax.axis("off")
    y = 0
    ax.set_xlim(0, 10)
    for fam in fam_order:
        group = [it for it in items if it[1] == fam]
        if not group:
            continue
        ax.text(0.0, y, fam_label[fam], fontsize=9.5, color=NAVY, va="center", **SERIF)
        for k, (iid, _, st, lb) in enumerate(group):
            cx = 3.1 + k * 0.62
            if lb:
                ax.scatter([cx], [y], s=760, c="none", edgecolors=INK, linewidths=1.6, zorder=2)
            ax.scatter([cx], [y], s=380, c=state_fc[st], edgecolors=state_fc[st], linewidths=0.8, zorder=3)
        ax.text(3.1 + len(group) * 0.62 + 0.15, y, f"{len(group)}", fontsize=8.5, color=SLATE, va="center")
        y -= 1
    ax.set_ylim(y, 1)
    # legend
    lx, ly = 0.05, 0.05
    for st, lab in (("closed", "closed or discharged"), ("open", "open"), ("partial", "half closed"), ("void", "void or superseded")):
        fig.patches.append(Circle((lx + 0.006, ly + 0.012), 0.006, transform=fig.transFigure, fc=state_fc[st], ec=state_fc[st]))
        fig.text(lx + 0.018, ly + 0.012, lab, va="center", fontsize=8, color=INK)
        lx += 0.14
    fig.patches.append(Circle((lx + 0.006, ly + 0.012), 0.0085, transform=fig.transFigure, fc="none", ec=INK, lw=1.2))
    fig.patches.append(Circle((lx + 0.006, ly + 0.012), 0.005, transform=fig.transFigure, fc=NAVY, ec=NAVY))
    fig.text(lx + 0.02, ly + 0.012, "load-bearing (outer ring)", va="center", fontsize=8, color=INK)

    # right column: the two blockers and the readiness word
    axr = fig.add_axes([0.70, 0.10, 0.27, 0.76])
    axr.axis("off")
    axr.set_xlim(0, 1)
    axr.set_ylim(0, 1)
    box(axr, 0.0, 0.50, 1.0, 0.48, fc=CREAM, ec=MIST, lw=0.8, r=0.03)
    axr.text(0.05, 0.945, f"Open on the live tracker, {gh['as_of']}", fontsize=10.5, color=NAVY, **SERIF)
    smoke = "; ".join(f"#{n}" for n, _ in gh["smoke_run_blockers"])
    unbuilt = ", ".join(f"#{n}" for n, _ in gh["unbuilt_before_the_route_gate"])
    owed = ", ".join(f"#{n}" for n, _ in gh["review_gate_owed"])
    axr.text(0.05, 0.885, f"Before the smoke proof ({smoke}): the elevated\n    one-cell run itself, and the machine-wide trace\n    provider the consumer must scope.", fontsize=7.6, color=INK, va="top")
    axr.text(0.05, 0.775, f"Unbuilt before the route gate ({unbuilt}): the\n    per-witness exactness runner, the three carriers\n    that are the experiment's subject, the 100-cell\n    grid runner, the provider route client.", fontsize=7.6, color=INK, va="top")
    axr.text(0.05, 0.635, f"A review gate still owed ({owed}).", fontsize=7.6, color=INK, va="top")
    axr.text(0.05, 0.575, f"{gh['open']} open of {gh['filed']} filed; {len(gh['closed_since_the_snapshot'])} closed since the\n    committed snapshot.", fontsize=7.6, color=SLATE, va="top", style="italic")
    box(axr, 0.0, 0.22, 1.0, 0.24, fc=NAVY, ec=NAVY, r=0.03)
    axr.text(0.5, 0.405, "readiness word the verifier prints today", fontsize=7.6, color=MIST, ha="center")
    axr.text(0.5, 0.325, "BUILD IMPLEMENTED", fontsize=11, color=PAPER, ha="center", fontweight="bold")
    axr.text(0.5, 0.255, "PRODUCTION AUTHORITY NOT ACTIVATED", fontsize=8.6, color=PAPER, ha="center")
    axr.text(0.0, 0.16, "Today's run of the repository (26 September 2026):\n601 tests, all passing; bundle verifier exit 0;\nfrozen 156 of 156; build 289 of 289;\nledger 118 invariants over 289 witnesses.",
             fontsize=7.6, color=INK, va="top")
    save(fig, "fig4-issue-ledger")


# ---------------------------------------------------------------- figure 5
def fig5(d):
    p = d["prereg"]
    fig = plt.figure(figsize=(12.4, 6.4))
    title(fig, "What it costs to press go, in calls, and why the number is what it is",
          "The design freezes call counts; it deliberately does not freeze a price. Dollar values are illustrative and are not part of the record.")
    ax = fig.add_axes([0.30, 0.16, 0.42, 0.66])
    rows = [
        ("route soak in the superseded r8 design", p["superseded_r8_soak_calls"], FOG, SLATE),
        (f"route gate in the registered design\n({p['route_trials']} six-call trials, pass at {p['route_max_failures']} or fewer failures)", p["route_scheduled_positions"], MIST, INK),
        (f"the experiment itself\n({p['n_pairs']} pairs x 6 positions)", p["scheduled_call_positions"], NAVY, PAPER),
        ("total scheduled calls before the one look", p["route_scheduled_positions"] + p["scheduled_call_positions"], AMBER, INK),
    ]
    ys = list(range(len(rows)))[::-1]
    for y, (lab, v, fc, tc) in zip(ys, rows):
        ax.barh(y, v, color=fc, height=0.62)
        ax.text(v + 900, y, f"{v:,}", va="center", fontsize=9.5, color=INK, fontweight="bold")
        ax.text(-1200, y, lab, va="center", ha="right", fontsize=8.2, color=INK)
    ax.set_xlim(0, 112000)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks([])
    ax.set_xlabel("scheduled model calls")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color=FOG)
    ax.text(p["route_scheduled_positions"] + 13000, ys[1] - 0.02,
            f"the council replaced the {p['superseded_r8_soak_calls']:,}-call soak with a {p['route_scheduled_positions']:,}-call binomial gate\n"
            f"that still accepts a 2% bad route with probability at most {math.ceil(p['bad_route_acceptance_max'] * 10000) / 10000:.4f}\n"
            f"and passes a 0.5% good route with probability at least {math.floor(p['good_route_acceptance_min'] * 1000) / 1000:.3f}",
            fontsize=7.6, color=INK, va="center")

    axr = fig.add_axes([0.76, 0.16, 0.21, 0.66])
    axr.axis("off")
    axr.set_xlim(0, 1)
    axr.set_ylim(0, 1)
    box(axr, 0, 0.0, 1, 1, fc=CREAM, ec=MIST, lw=0.8, r=0.03)
    axr.text(0.06, 0.93, "Illustrative only", fontsize=10.5, color=NAVY, **SERIF)
    total = p["route_scheduled_positions"] + p["scheduled_call_positions"]
    axr.text(0.06, 0.85, f"{total:,} calls at an assumed all-in\nprice per call:", fontsize=7.8, color=INK, va="top")
    for i, price in enumerate((0.10, 0.50, 2.00)):
        yy = 0.66 - i * 0.16
        axr.text(0.08, yy, f"${price:.2f}", fontsize=10, color=NAVY, **SERIF)
        axr.text(0.92, yy, f"${total * price:,.0f}", fontsize=10, color=INK, ha="right", fontweight="bold")
        axr.plot([0.06, 0.94], [yy - 0.05, yy - 0.05], color=MIST, lw=0.6)
    axr.text(0.06, 0.16, "Values are illustrative. Prices, token ceilings and\nretry ceilings are frozen and approved before the\nroute gate runs inside that ceiling; the paid run\nneeds its own authorization after the gates.",
             fontsize=7.2, color=SLATE, va="top", style="italic")
    save(fig, "fig5-calls-and-cost")


if __name__ == "__main__":
    d = load()
    for fn in (fig1, fig2, fig3, fig4, fig5):
        fn(d)
    print("done ->", OUT)
