# License Compliance Auditor

> 🚧 **Work in progress.** The ingestion layer is built; the agent pipeline is under active construction. See [Status](#status).

A multi-agent system that reads a code repository, detects and classifies its open-source licenses, and flags obligation conflicts — combining deterministic SPDX-matrix reasoning with LLM-based extraction.

## The problem

License compliance is a judgment call, not a lookup. A repo's license terms can be scattered across a `LICENSE` file, manifest fields (`package.json`, `pyproject.toml`), source headers, `NOTICE` files, and a vague README mention — often in conflict with each other. Getting it wrong is expensive: shipping GPL-obligated code in a proprietary product, or mixing incompatible licenses across a dependency tree, creates real legal exposure.

The hard part is three layers of ambiguity:

1. **Detection** — where the license information actually lives, given no consistent schema.
2. **Classification** — mapping messy real-world text to one of ~600 SPDX identifiers.
3. **Obligation reasoning** — chaining what a license *requires* against how the code is *used* (static linking vs. SaaS vs. distribution) across the whole dependency tree.

That last layer is why this is a multi-agent problem rather than a single API call.

## Architecture (planned)

```
Repo input (GitHub URL / local manifest)
        │
   Router Agent  ── zero-shot: clean LICENSE? ambiguous? conflicting signals?
        │
   ┌────┴────────────┬─────────────────────┐
 Extraction       Classification        Conflict Detection
 (Document QA     (embedding shortlist  (sentence similarity vs.
  over README,     → zero-shot pick      known conflicting patterns:
  manifests,       among top-10 SPDX)    dual-license, vendored subtree)
  NOTICE files)
   └────┬────────────┴─────────────────────┘
        │
   Obligation Reasoning Agent  ── query SPDX compatibility matrix,
        │                          chain obligations across deps
   Synthesis + Citation  ── report citing the exact license file line per claim
```

Two-stage classification is deliberate: zero-shot degrades badly across ~600 candidate classes, so embedding similarity narrows to a top-10 shortlist first, then zero-shot picks among those.

## Status

| Component | State |
|---|---|
| Repo input layer (list root files via GitHub API) | ✅ built |
| Candidate license-source detection | ✅ built |
| Router agent | ⬜ planned |
| Extraction agent (Document QA) | ⬜ planned |
| Classification agent (embedding + zero-shot) | ⬜ planned |
| Conflict detection agent | ⬜ planned |
| Obligation reasoning + SPDX matrix | ⬜ planned |
| Synthesis + citation report | ⬜ planned |

Built so far: [`ingest.py`](ingest.py) — lists a repo's root files through the GitHub contents API and flags likely license sources (`LICENSE`, `NOTICE`, `COPYING`, `README`, and package manifests).

## Stack

Python (standard library for ingestion), SPDX License List, GitHub / package-registry APIs, and an LLM agent layer for extraction, classification, and obligation reasoning.
