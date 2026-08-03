# Threat model

## Assets and trust assumptions

The protected asset is the integrity of the stored outcome. The contract assumes
a GenLayer validator majority follows the protocol, public URLs are reachable,
and the caller supplies criteria that can be evaluated from those URLs.

## Threats and mitigations

### Malicious or hallucinating leader

Validators refetch and reevaluate evidence independently. Format-only validation
is insufficient and is not used.

### Prompt injection in source pages

The prompt explicitly labels pages as untrusted evidence and instructs the model
not to follow embedded instructions. Independent validators reduce, but cannot
eliminate, shared-model susceptibility.

### Sybil sources and duplicated reporting

Exact duplicate URLs are rejected and the evaluator is told to count only
substantively independent sources. Domain diversity is not mechanically enforced;
a domain allowlist or registrable-domain check is recommended for high stakes.

### Source mutation and timing races

Validators can observe different page versions. Bounded count/confidence
tolerances help liveness, while exact outcome equality prevents conflicting
settlement. Archival or content-addressed sources are preferable.

### Unavailable sources

Failures become `[UNAVAILABLE]`; fewer than two usable sources forces
`INCONCLUSIVE`. The contract does not fabricate missing evidence.

### Cost and denial of service

Claim, criteria, URL length, source count, fetched excerpt, and rationale are
bounded. Rendering up to five sites plus LLM evaluation remains intentionally
expensive and should be rate-limited or fee-gated by downstream applications.

### SSRF and unsafe URLs

HTTPS is required, but this contract does not implement IP-range or DNS rebinding
checks. GenVM's network sandbox is an important boundary. Production forks should
use source allowlists where available.

### Ambiguous or adversarial criteria

The contract cannot rescue vague criteria. `INCONCLUSIVE` is the safe terminal
outcome. Applications should template criteria and display them before users
commit value.

## Out of scope

Compromised validator majorities, private evidence, legal enforceability,
copyright compliance of caller-selected pages, and correctness after a source is
changed retroactively are outside this primitive's guarantees.
