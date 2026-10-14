"""Run every prompt through every model, a few times each, and score it.

    python run_eval.py                                   # keyless: 3 mock models, 3 runs each
    python run_eval.py --local --models llama3.2         # your own Ollama model, no key
    python run_eval.py --provider openrouter --models anthropic/claude-haiku-4.5,meta-llama/llama-3.3-70b-instruct
    python run_eval.py --provider gateway --models openai/gpt-5-mini
    LLM_BASE_URL=https://... python run_eval.py --provider custom --models my-model

Answers land in results/<model>.jsonl. Then run compare.py.
"""

import argparse
import json
import sys
from pathlib import Path

from evals.models import MOCK_MODELS, PROVIDERS, chat_answer, mock_answer
from evals.scorers import score

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def load_prompts(limit=None):
    lines = (ROOT / "data" / "civic_prompts.jsonl").read_text().splitlines()
    items = [json.loads(line) for line in lines if line.strip()]
    return items[:limit] if limit else items


def pct(values):
    return f"{100 * sum(values) / len(values):5.1f}%" if values else "   --"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--provider", default="mock", choices=["mock", *PROVIDERS])
    parser.add_argument("--models", help="comma-separated model IDs (default: the 3 mock models)")
    parser.add_argument("--local", action="store_true", help="shortcut for --provider ollama")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--limit", type=int, help="only the first N prompts (cheap smoke test)")
    args = parser.parse_args()

    provider = "ollama" if args.local else args.provider
    if provider == "mock":
        models = args.models.split(",") if args.models else list(MOCK_MODELS)
    elif args.models:
        models = args.models.split(",")
    else:
        sys.exit("Pick at least one model with --models (e.g. --models llama3.2).")

    items = load_prompts(args.limit)
    RESULTS.mkdir(exist_ok=True)
    for old in RESULTS.glob("*.jsonl"):
        old.unlink()

    safe_written = True
    print(f"{len(items)} prompts x {len(models)} models x {args.runs} runs  (provider: {provider})\n")
    print(f"{'model':<36} {'run':>3}  {'Right':>6}  {'Safe':>6}")
    for model in models:
        rows = []
        for run in range(1, args.runs + 1):
            right, safe = [], []
            for item in items:
                if provider == "mock":
                    answer = mock_answer(model, item, run)
                else:
                    answer = chat_answer(provider, model, item)
                s = score(item, answer)
                right.append(s["right"])
                if s["safe"] is None:
                    safe_written = False
                else:
                    safe.append(1.0 if s["safe"] else 0.0)
                rows.append({"model": model, "id": item["id"], "run": run, "answer": answer, **s})
            print(f"{model:<36} {run:>3}  {pct(right):>6}  {pct(safe):>6}")

        by_prompt = {}
        for r in rows:
            by_prompt.setdefault(r["id"], set()).add(r["right"])
        steady = sum(len(v) == 1 for v in by_prompt.values()) / len(by_prompt)
        print(f"{'':<36} Steady: same Right score on every run for {100 * steady:.0f}% of prompts\n")

        out = RESULTS / (model.replace("/", "__") + ".jsonl")
        out.write_text("".join(json.dumps(r) + "\n" for r in rows))

    if not safe_written:
        print("Safe shows -- because score_safe isn't written yet. That's your job in evals/safety.py.")
    print("Next: python compare.py")


if __name__ == "__main__":
    main()
