"""Is model A really better than model B, or is it just the jiggle?

    python compare.py                    # compares every model to the first one
    python compare.py --baseline model-b

How it works (you don't need the math): for each prompt we take each model's
average score across runs, then reshuffle the 20 prompts 5,000 times to see how
much the difference wobbles. If the whole wobble range stays on one side of
zero, the difference is real. If it crosses zero, it's noise.
"""

import argparse
import json
import random
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"


def load():
    per_model = {}
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            r = json.loads(line)
            per_model.setdefault(r["model"], []).append(r)
    return per_model


def prompt_means(rows, metric):
    scores = {}
    for r in rows:
        if r[metric] is None:
            return None
        scores.setdefault(r["id"], []).append(float(r[metric]))
    return {pid: sum(v) / len(v) for pid, v in scores.items()}


def bootstrap(diffs, n=5000, seed=6):
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(diffs, k=len(diffs))) / len(diffs) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def verdict(lo, hi):
    if lo > 0:
        return "REAL: really better"
    if hi < 0:
        return "REAL: really worse"
    return "noise: within the jiggle"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline")
    args = parser.parse_args()

    per_model = load()
    if not per_model:
        raise SystemExit("No results yet. Run: python run_eval.py")
    models = list(per_model)
    base = args.baseline or models[0]

    for metric in ("right", "safe"):
        base_scores = prompt_means(per_model[base], metric)
        if base_scores is None:
            print(f"\n{metric.title()}: skipped (write score_safe in evals/safety.py first)")
            continue
        print(f"\n{metric.title()}  (baseline: {base})")
        print(f"{'model':<36} {'score':>6}  {'vs baseline':>12}  {'95% range':>16}  verdict")
        for model in models:
            scores = prompt_means(per_model[model], metric)
            mean = 100 * sum(scores.values()) / len(scores)
            if model == base:
                print(f"{model:<36} {mean:5.1f}%  {'baseline':>12}")
                continue
            diffs = [scores[pid] - base_scores[pid] for pid in base_scores]
            lo, hi = bootstrap(diffs)
            delta = 100 * sum(diffs) / len(diffs)
            rng_txt = f"{100 * lo:+.1f} to {100 * hi:+.1f}"
            print(f"{model:<36} {mean:5.1f}%  {delta:+11.1f}%  {rng_txt:>16}  {verdict(lo, hi)}")

    print("\nRead the verdict column, not the score column. A few points of difference on 20 prompts is usually noise.")


if __name__ == "__main__":
    main()
