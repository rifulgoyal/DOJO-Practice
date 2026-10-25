#!/usr/bin/env python3
"""
Dojo Practice bot.

1. Finds RAW screenshots (any .png/.jpg that is not already question.jpg / solution.jpg)
   inside  <LANGUAGE>/WORKOUT/  or  <LANGUAGE>/DOJO/
2. Splits each one into the question half (left) and the solution half (right)
3. Saves them as  .../<problem-name>/question.jpg  and  .../<problem-name>/solution.jpg
4. Deletes the raw file
5. Rebuilds the stats in README.md and one index page per language (<LANGUAGE>/README.md)

Raw filename tips:
  JAVA/WORKOUT/L3__Number-pattern.png   -> JAVA/WORKOUT/LEVEL-3/Number-pattern/
  JAVA/WORKOUT/Number-pattern.png       -> JAVA/WORKOUT/Number-pattern/   (level not set yet)
  JAVA/DOJO/Frog-step-counter.png       -> JAVA/DOJO/Frog-step-counter/
"""
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EXTS = {".png", ".jpg", ".jpeg"}
SECTIONS = {"WORKOUT", "DOJO"}
PROCESSED_NAMES = {"question", "solution"}
DEFAULT_SPLIT = 0.35  # fallback: question panel is ~35% of the window width
LEVEL_PREFIX = re.compile(r"^[Ll](\d+)__(.+)$")
LEVEL_DIR = re.compile(r"^LEVEL-(\d+)$", re.I)


# --------------------------------------------------------------------------
# Splitting
# --------------------------------------------------------------------------
def find_split_x(img: Image.Image) -> int:
    """Find the dark vertical divider between the question panel and the editor.

    Looks for the first thin dark column with lighter pixels on both sides,
    somewhere between 25% and 50% of the width. Falls back to a fixed 35% split.
    """
    gray = np.asarray(img.convert("L"), dtype=np.float32)
    h, w = gray.shape
    band = gray[int(h * 0.35):int(h * 0.85), :]
    col = band.mean(axis=0)
    # A real divider is dark on (almost) every row; a hand-drawn blur/redaction box is not.
    dark_frac = (band < 110).mean(axis=0)

    scores = {}
    for x in range(int(w * 0.25), int(w * 0.50)):
        left = col[max(0, x - 8):x - 2]
        right = col[x + 3:x + 9]
        if len(left) == 0 or len(right) == 0:
            continue
        if dark_frac[x] < 0.85:
            continue
        scores[x] = min(left.mean(), right.mean()) - col[x]

    # The FIRST strong dark line is the panel divider (a second one, further
    # right, is the edge of the code editor's line-number gutter).
    for x in sorted(scores):
        if scores[x] > 40:
            window = [k for k in range(x, x + 6) if k in scores]
            return max(window, key=lambda k: scores[k])
    return int(w * DEFAULT_SPLIT)


def slugify(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_-]+", "-", name.strip())
    return re.sub(r"-{2,}", "-", name).strip("-") or "question"


def process_new_images() -> int:
    raw_files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        rel = path.relative_to(ROOT)
        if len(rel.parts) < 3:  # must be LANG/SECTION/file
            continue
        if rel.parts[1].upper() not in SECTIONS:
            continue
        if path.stem.lower() in PROCESSED_NAMES:
            continue
        raw_files.append(path)

    done = 0
    for path in sorted(raw_files):
        rel = path.relative_to(ROOT)
        section_dir = ROOT / rel.parts[0] / rel.parts[1]
        stem = path.stem

        level = None
        m = LEVEL_PREFIX.match(stem)
        if m:
            level, stem = int(m.group(1)), m.group(2)
        else:
            for part in rel.parts[2:-1]:
                lm = LEVEL_DIR.match(part)
                if lm:
                    level = int(lm.group(1))

        problem = slugify(stem)
        if rel.parts[1].upper() == "WORKOUT" and level is not None:
            dest = section_dir / f"LEVEL-{level}" / problem
        else:
            dest = section_dir / problem

        n = 2
        base = dest
        while dest.exists():
            dest = base.with_name(f"{base.name}-{n}")
            n += 1

        try:
            img = Image.open(path).convert("RGB")
        except Exception as exc:  # corrupt upload
            print(f"SKIP {rel}: cannot open ({exc})", file=sys.stderr)
            continue

        w, h = img.size
        x = find_split_x(img)
        dest.mkdir(parents=True)
        img.crop((0, 0, x, h)).save(dest / "question.jpg", quality=90)
        img.crop((x, 0, w, h)).save(dest / "solution.jpg", quality=90)
        path.unlink()
        print(f"SPLIT {rel} at x={x}/{w} -> {dest.relative_to(ROOT)}")
        done += 1
    return done


# --------------------------------------------------------------------------
# Collecting + generating docs
# --------------------------------------------------------------------------
def collect():
    items = []
    for q in ROOT.rglob("question.jpg"):
        rel = q.relative_to(ROOT)
        if len(rel.parts) < 4 or rel.parts[1].upper() not in SECTIONS:
            continue
        level = None
        for part in rel.parts[2:-2]:
            lm = LEVEL_DIR.match(part)
            if lm:
                level = int(lm.group(1))
        items.append({
            "lang": rel.parts[0],
            "section": rel.parts[1].upper(),
            "level": level,
            "name": rel.parts[-2].replace("-", " ").replace("_", " "),
            "dir": q.parent,
        })
    return items


def img_tag(path: Path, base: Path) -> str:
    rel = os.path.relpath(path, base).replace(os.sep, "/")
    return f'<img src="{quote(rel)}" loading="lazy" width="100%">'


def render_group(group, base: Path):
    out = []
    for it in sorted(group, key=lambda i: i["name"].lower()):
        out += [
            "<details>",
            f"<summary><b>{it['name']}</b></summary>",
            "<br>",
            img_tag(it["dir"] / "question.jpg", base),
            "<details>",
            "<summary>👀 Show solution</summary>",
            "<br>",
            img_tag(it["dir"] / "solution.jpg", base),
            "</details>",
            "</details>",
            "",
        ]
    return out


def build_language_page(lang: str, items):
    base = ROOT / lang
    lines = [
        f"# {lang} questions",
        "",
        "> 🤖 Auto-generated by the repo bot — please don't edit by hand. "
        "Open a question, try it yourself, then click **Show solution**.",
        "",
        f"**{len(items)} questions** in this language.",
        "",
    ]
    for section in ("WORKOUT", "DOJO"):
        sec = [i for i in items if i["section"] == section]
        if not sec:
            continue
        lines += [f"## {section.title()} ({len(sec)})", ""]
        if section == "WORKOUT":
            levels = sorted({i["level"] for i in sec}, key=lambda l: (l is None, l or 0))
            for lv in levels:
                group = [i for i in sec if i["level"] == lv]
                title = f"Level {lv}" if lv is not None else "Level not set yet"
                lines += [f"### {title} ({len(group)})", ""]
                lines += render_group(group, base)
        else:
            lines += render_group(sec, base)
    (base / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_stats(items) -> str:
    langs = sorted({i["lang"] for i in items})
    rows = ["| Language | Workout | Dojo | Total |", "|----------|--------:|-----:|------:|"]
    for lang in langs:
        mine = [i for i in items if i["lang"] == lang]
        wk = sum(1 for i in mine if i["section"] == "WORKOUT")
        dj = sum(1 for i in mine if i["section"] == "DOJO")
        rows.append(f"| [{lang}]({quote(lang)}/) | {wk} | {dj} | {len(mine)} |")
    no_level = sum(1 for i in items if i["section"] == "WORKOUT" and i["level"] is None)
    text = "\n".join(rows)
    if no_level:
        text += f"\n\n> ⚠️ **{no_level}** workout question(s) don't have a level yet. Help by moving them into a `LEVEL-N` folder!"
    return text


def sub_marker(text: str, start: str, end: str, value: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    return pattern.sub(lambda _: f"{start}{value}{end}", text)


def update_readme(items):
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    count = len(items)
    date = datetime.now(timezone.utc).strftime("%d %b %Y")
    badge = f"![Questions](https://img.shields.io/badge/Questions-{count}-blue)"
    text = sub_marker(text, "<!--COUNT_START-->", "<!--COUNT_END-->", str(count))
    text = sub_marker(text, "<!--DATE_START-->", "<!--DATE_END-->", date)
    text = sub_marker(text, "<!--BADGE_START-->", "<!--BADGE_END-->", badge)
    text = sub_marker(text, "<!--STATS_START-->", "<!--STATS_END-->", "\n" + build_stats(items) + "\n")
    readme.write_text(text, encoding="utf-8")


def main():
    split = process_new_images()
    items = collect()
    for lang in sorted({i["lang"] for i in items}):
        build_language_page(lang, [i for i in items if i["lang"] == lang])
    update_readme(items)
    print(f"Done. Split {split} new screenshot(s). Total questions: {len(items)}")


if __name__ == "__main__":
    main()
