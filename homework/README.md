# Week 6 homework: add one eval to your hackathon idea

**Due before Build Weekend starts, Fri Oct 23.** Submit in Google Classroom.

A working demo with one eval beats a big demo nobody tested. "Done" at Demo Day means: it works on synthetic data, **it passed your eval**, and it cleared the safety checklist.

## What to do

1. **Pick the scariest failure.** What would be most embarrassing if your project got it wrong on stage?
2. **Write 5 to 10 test cases** for it. Include one easy case, one hard case, and one that tries to break it. Synthetic data only.
3. **Pick the cheapest scorer that works:** contains / exact match, then schema check, then rubric, then LLM judge.
4. **Set your threshold before you run it** (e.g. "9 of 10 Right, 10 of 10 Safe").
5. **Run it 3 times.** Write down all three scores. Did they move?
6. **Fill in [`eval-template.md`](eval-template.md).**

Stuck? Open this repo with your coding agent and say: *"Help me with the Week 6 homework."* The skill file at `.claude/skills/eval-practice/SKILL.md` makes it coach you through it, one question at a time.

## Submit

- Your filled-in `eval-template.md`
- Your eval: code, a notebook, **or a spreadsheet** (inputs, expected, actual, pass/fail). No-code counts.
- A screenshot of your three runs

Any AI provider works, including a mock. Nothing here requires a paid key.
