# 🥋 Kalvium Dojo Practice

A community-built collection of **Kalvium Coding Workout and Dojo questions**, each with the question and a working solution. Attempted a question? Add a screenshot and help the next student.

<!--BADGE_START--><img src="https://img.shields.io/badge/Questions-10-blue" alt="Questions"><!--BADGE_END-->
![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen)

---

## 📊 Live Stats

**Total questions: <!--COUNT_START-->10<!--COUNT_END-->** · Last updated: <!--DATE_START-->27 Oct 2026<!--DATE_END-->

<!--STATS_START-->

| Language | Workout | Dojo | Total |
|----------|--------:|-----:|------:|
| [JAVA](JAVA/) | 3 | 2 | 5 |
| [JS](JS/) | 1 | 0 | 1 |
| [PYTHON](PYTHON/) | 4 | 0 | 4 |

<!--STATS_END-->

Click a language above to browse its questions. Every question shows the problem first, and the solution stays hidden until you click **Show solution**, so you can try it yourself first.

> These numbers and pages are generated automatically by a bot. Never edit them by hand.

---

## 🆘 Help Wanted

- **Dojo questions**: if you have attempted a Dojo (main test), your screenshots are the most valuable thing you can add here.
- **Workout questions**: any level, any language.
- **More languages**: Java and Python are covered so far. CSS and JavaScript are coming, and help is welcome.
- **Missing levels**: some older workout questions don't have a level yet. If you know the level of one, move it into the right `LEVEL-N` folder.

---
## 🔍 Screenshot format

The bot expects a full-window screenshot about twice as wide as it is tall, with the question on the left and the code on the right. If your screenshot doesn't match, it isn't lost. It goes into [`_needs-review`](_needs-review/) and a maintainer will check it and sort it manually.

## 🤝 How to Contribute (no cropping or editing needed)

You only upload **one normal full-window screenshot** with the question on the left and your code on the right. A bot splits it into a question image and a solution image, files it in the right place, and updates the counter.

### Step 1: Take the screenshot
- Capture the **whole browser window**: question on the left, editor on the right.
- Don't crop it, and don't change the layout.
- Make the code visible and the question readable.

### Step 2: Hide personal info ⚠️
The bot can't do this for you. Before uploading, blur or cover:
- your name, email, or profile picture
- other browser tabs (mail, personal sites)
- the taskbar and anything else personal

### Step 3: Name your file
| Type | Where to upload | File name example |
|------|-----------------|-------------------|
| Workout | `<LANGUAGE>/WORKOUT/` | `L3__Number-pattern.png` |
| Dojo | `<LANGUAGE>/DOJO/` | `Frog-step-counter.png` |

- For workouts, start the name with **`L` + level number + two underscores** (`L3__`). That puts it in the right level automatically.
- Use hyphens, not spaces: `Binary-to-decimal`, not `Binary to decimal`.
- If you don't know the level, leave the prefix off and it will be listed as "Level not set yet".

### Step 4: Upload
**From the browser:**
1. Open the correct folder (for example `JAVA/WORKOUT`).
2. Click **Add file → Upload files** and drop in your screenshot.
3. Choose **Create a new branch and start a pull request**, then click **Propose changes**.

**With Git:**
```bash
git clone https://github.com/rifulgoyal/DOJO-Practice.git
cd DOJO-Practice
git checkout -b add-java-number-pattern
cp ~/Downloads/L3__Number-pattern.png JAVA/WORKOUT/
git add . && git commit -m "Add: Java workout L3 Number-pattern"
git push origin add-java-number-pattern
```
Then open a Pull Request.

### What happens next
After your PR is merged, the bot:
1. splits your screenshot into `question.jpg` and `solution.jpg`
2. files them as `<LANGUAGE>/WORKOUT/LEVEL-3/Number-pattern/`
3. deletes the raw upload
4. updates the counter and the language page

---

## 📁 Folder Structure

```
.
├── JAVA/
│   ├── README.md                  ← auto-generated question list
│   ├── WORKOUT/
│   │   └── LEVEL-3/
│   │       └── Number-pattern/
│   │           ├── question.jpg
│   │           └── solution.jpg
│   └── DOJO/
│       └── Frog-step-counter/
│           ├── question.jpg
│           └── solution.jpg
├── PYTHON/
│   └── ...
├── scripts/process.py             ← the bot's script
└── .github/workflows/process-screenshots.yml
```

To add a **new language**, create a folder for it with `WORKOUT` and `DOJO` inside, or open an issue and ask.

---

## ✅ Pull Request Checklist

- [ ] The screenshot shows the full window (question left, code right)
- [ ] Personal info is blurred or covered
- [ ] The file is in `<LANGUAGE>/WORKOUT/` or `<LANGUAGE>/DOJO/`
- [ ] The file name uses hyphens, with an `L<number>__` prefix for workouts
- [ ] The question isn't already in the repo (search first)
- [ ] The solution passes the test cases

---

## ⚠️ Disclaimer

This is an **unofficial, student-run** repository, not affiliated with or endorsed by Kalvium. It is for learning and practice, so please use it to understand the solutions and not to copy them blindly. Make sure sharing a question doesn't break your course or assessment rules. If you are a rights holder and want something removed, open an issue and it will be taken down promptly.

---

<p align="center">If this repo helped you, give it a ⭐ so others can find it!</p>
