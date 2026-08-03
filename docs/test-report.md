# Test report

Validated on 2026-08-03 in an isolated Ubuntu VM.

## Verified toolchain

- Python 3.14.4
- `pytest` 9.1.1
- `genlayer-test` 0.29.2
- GenVM SDK/runner pinned by the Direct Mode tests to `v0.2.12`

## Results

```text
genvm-lint check contracts/EvidenceQuorumResolver.py
✓ Lint passed (3 checks)
✓ Validation passed
  Contract: EvidenceQuorumResolver
  Methods: 3 (2 view, 1 write)

pytest tests/direct -v
6 passed in 0.15s
```

The six Direct Mode tests cover initialization, invalid source sets, accepted
settlement persistence, bounded independent-validator variation, and rejection
when a validator derives the opposite outcome.

## Compatibility note

The linter reported that a newer `py-genlayer` runner exists. This repository
keeps the tested dependency header and Direct Mode SDK pin until the newer
runner is reviewed and the full suite passes against it. This favors a
reproducible tested baseline over an unverified automatic upgrade.

## Remaining validation

Studio integration is intentionally opt-in and still needs a running GenLayer
Studio/localnet with validators and live web/LLM access:

```bash
RUN_STUDIO_TESTS=1 gltest tests/integration -v -s --network localnet
```
