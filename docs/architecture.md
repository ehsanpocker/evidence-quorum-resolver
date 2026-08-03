# Architecture

## Purpose

EvidenceQuorum Resolver is a neutral settlement primitive. Callers define a
claim, explicit resolution criteria, and a bounded source set. The contract
turns that evidence into one durable, queryable state transition.

## Flow

1. Deterministic input checks reject oversized, duplicate, non-HTTPS, or
   insufficient source lists.
2. The leader renders each source as text inside a nondeterministic block.
3. The leader's LLM classifies each source and proposes a structured decision.
4. Validators independently refetch and reevaluate all evidence.
5. The custom validator compares outcome, directional counts, usable-source
   count, and confidence tolerance.
6. Only an accepted result is written to `resolutions`; rejected or
   undetermined executions produce no state transition.

## State model

`next_id` is monotonic. `resolutions` maps the string representation of each ID
to an immutable `Resolution`. Each record keeps its original claim and criteria,
canonical source JSON, outcome, evidence statistics, compact audit metadata,
requester, and resolved flag.

There is no update or delete method. This makes accepted decisions append-only
and prevents administrative rewriting. The `owner` is recorded for future
versioning but has no privileged settlement power.

## Reuse

Downstream contracts can treat the returned ID and outcome as an oracle-like
primitive. A production composition may add callbacks or escrow transfers, but
they are intentionally omitted here so this submission remains standalone and
auditable.

## Boundaries

The resolver does not discover sources, adjudicate private evidence, transfer
funds, or claim legal authority. Source selection and criteria quality remain
caller responsibilities.
