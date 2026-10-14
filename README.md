# Test It Before You Trust It

**3percentclub · AI Builders · Week 6 lab: Evals, guardrails & system architecture**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/3percentclub/builders-week6-evals/blob/main/lab.ipynb)

Same 20 civic prompts, three models, three runs each. Then the real question: **is model A actually better than model B, or is that just the jiggle?**

**No API key. No account. No cost.** Click the badge, press play on each box, top to bottom.

## Right, Safe, Steady

Every eval tonight checks one of three things:

| | Question | How this repo measures it |
|---|---|---|
| **Right** | Did it get the answer correct? | Does the answer contain the expected facts? (`evals/scorers.py`) |
| **Safe** | Did it stay inside the guardrails? | Does it leak an email or a private phone number? (`evals/safety.py`, **you write this one**) |
| **Steady** | Same quality on run two, three, twenty? | Every prompt runs 3 times; `run_eval.py` reports how often the score held |

## What's in here

```
data/city_guide.md        a made-up NYC-style programs guide (all fake on purpose)
data/civic_prompts.jsonl  20 prompts: 17 questions + 3 that try to pull personal info
evals/models.py           where answers come from (mock by default, any provider optional)
evals/scorers.py          the Right check
evals/safety.py           the Safe check (YOUR TURN)
run_eval.py               every prompt -> every model, 3 runs each
compare.py                is the difference real or noise?
find_the_mistake/         the pairs exercise from class
homework/                 add one eval to your hackathon idea
.claude/skills/eval-practice/SKILL.md   your agent coaches you through the homework
```

## Run it (Colab, Codespaces, or your laptop)

```bash
python run_eval.py      # every prompt -> every model, 3 runs each
python compare.py       # is A really better than B?
python -m pytest -q     # check your Safe scorer (goal: 5 passed)
```

Only `pytest` is needed (`pip install -r requirements.txt`). Everything else is the Python standard library.

## Works with any AI provider

The default "models" are three seeded mock models in `evals/models.py`. They act like real ones (sometimes they drop a fact, sometimes they leak personal info), and everyone in the room gets the same numbers.

When you want real models, point the same harness at **any provider with an OpenAI-style chat API**. The scorers and `compare.py` don't change:

```bash
python run_eval.py --local --models llama3.2                    # Ollama on your machine, no key
OPENROUTER_API_KEY=... python run_eval.py --provider openrouter --models <model-a>,<model-b>
AI_GATEWAY_API_KEY=... python run_eval.py --provider gateway --models <provider/model>
LLM_BASE_URL=... LLM_API_KEY=... python run_eval.py --provider custom --models <model>
```

Use `--limit 3` for a cheap smoke test first. Heads up: the Right check looks for exact phrases, so a real model saying "9 a.m." instead of "9am" scores as a miss. Cheap scorers are fast and free, but brittle. Spotting that is part of the lesson.

## Homework

**Add one eval to your hackathon idea** before Build Weekend (Fri Oct 23). See [`homework/README.md`](homework/README.md).

---

All data here is synthetic. Never put real people's information into a test set.
