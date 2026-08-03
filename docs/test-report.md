# Test report

Validated on 2026-08-04 in an isolated Ubuntu VM.

## Verified toolchain

- Python 3.14.4
- `pytest` 9.1.1
- `genlayer-test` 0.29.2
- GenVM SDK/runner pinned by the Direct Mode tests to `v0.2.12`

## Results

### Contract lint and validation

```text
genvm-lint check contracts/EvidenceQuorumResolver.py
✓ Lint passed (3 checks)
✓ Validation passed
  Contract: EvidenceQuorumResolver
  Methods: 3 (2 view, 1 write)
```

### Direct Mode

```text
pytest tests/direct -v
6 passed in 0.15s
```

The six Direct Mode tests cover initialization, invalid source sets, accepted
settlement persistence, bounded independent-validator variation, and rejection
when a validator derives the opposite outcome.

### Studionet integration

```text
RUN_STUDIO_TESTS=1 gltest tests/integration -v -s --network studionet
1 passed in 64.75s (0:01:04)
```

The integration test deployed `EvidenceQuorumResolver` to the hosted GenLayer
Studionet, verified the initial state, submitted a live claim backed by the IANA
example-domain page and RFC 2606, waited for consensus acceptance, and confirmed
that the resolution was persisted.

A first attempt on 2026-08-03 was blocked before deployment because the public
Studionet endpoint had reached its 5,000-request daily limit. The successful
run above completed after the service quota reset; no contract change was
required.

## Compatibility note

The linter reported that a newer `py-genlayer` runner exists. This repository
keeps the tested dependency header and Direct Mode SDK pin until the newer
runner is reviewed and the full suite passes against it. This favors a
reproducible tested baseline over an unverified automatic upgrade.

## Reproduce

Direct Mode:

```bash
pytest tests/direct -v
```

Hosted Studionet integration:

```bash
RUN_STUDIO_TESTS=1 gltest tests/integration -v -s --network studionet
```

The Studionet test performs live deployment, web requests, and LLM consensus,
so it is opt-in and depends on the availability and rate limits of the hosted
service.
