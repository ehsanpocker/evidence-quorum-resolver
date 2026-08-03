# Consensus design

## Why custom leader/validator logic

Exact equality is too brittle for LLM-derived analysis, while a validator that
checks only JSON shape would trust the leader. The contract therefore uses
`gl.vm.run_nondet_unsafe` and requires each validator to perform the substantive
work again from the original web evidence.

## Leader result

The leader returns canonical JSON containing:

- `outcome`: the shared-state decision
- supporting, contradicting, and usable-source counts
- confidence from 0 to 100
- compact evidence identifier and rationale

The prompt treats fetched pages as untrusted data and encodes deterministic
safety floors. A positive or negative outcome requires at least two usable
sources, confidence of 70+, and the corresponding directional majority.

## Validator equivalence

The validator independently calls the full evaluator. It accepts only when:

- the outcome matches exactly;
- each evidence count differs by at most one;
- confidence differs by at most 15 points; and
- basic range and size invariants still hold.

The rationale and digest are not equality fields because prose and extracted
fact wording can vary without changing settlement. They remain audit aids, not
consensus anchors.

## Failure behavior

Malformed LLM output, an exception result, missing fields, or a materially
different independent decision causes rejection. Network-level leader rotation
can retry. If validators cannot converge, the transaction becomes undetermined
and storage is unchanged. `INCONCLUSIVE` is a valid accepted outcome when the
independent evaluations agree that evidence is insufficient.

## Trade-offs

A count tolerance improves liveness when one source is temporarily unavailable,
but exact outcome agreement preserves safety. For high-value deployments,
source-domain allowlists, time snapshots, and domain-specific parsers should be
added in a specialized fork.
