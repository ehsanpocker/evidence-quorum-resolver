# EvidenceQuorum Resolver

A standalone GenLayer Intelligent Contract primitive that resolves bounded,
publicly verifiable claims from 2–5 independent HTTPS sources. It is designed
for reuse by prediction markets, milestone escrows, bounties, insurance flows,
reputation systems, and DAOs.

The contract is intentionally **not** a frontend and **not** a thin LLM wrapper.
The leader fetches and evaluates evidence; every validator fetches the same
sources and makes an independent evaluation. State changes only after the
custom equivalence check accepts the leader's substantive result.

## What is included

- `contracts/EvidenceQuorumResolver.py` — deployable contract
- `tests/direct/` — fast state, validation, and consensus tests
- `tests/integration/` — opt-in Studio/localnet test
- `docs/` — architecture, consensus design, threat model, and setup guide
- `examples/claims.json` — reusable input shapes
- `gltest.config.yaml` — localnet and Studionet endpoints

## Quick start (Direct Mode)

Requirements: Git and Python 3.12 or newer. Python 3.13 may work, but 3.12 is
the documented GenLayer baseline.

### Windows PowerShell

```powershell
git clone https://github.com/YOUR_USERNAME/evidence-quorum-resolver.git
cd evidence-quorum-resolver
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
genvm-lint check contracts/EvidenceQuorumResolver.py
pytest tests/direct -v
```

### macOS/Linux

```bash
git clone https://github.com/YOUR_USERNAME/evidence-quorum-resolver.git
cd evidence-quorum-resolver
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
genvm-lint check contracts/EvidenceQuorumResolver.py
pytest tests/direct -v
```

## Local GenLayer Studio

Install Node.js 18+, Docker 26+, and the GenLayer CLI, then:

```bash
npm install -g genlayer
genlayer init --numValidators 5
genlayer up --numValidators 5
```

Open `http://localhost:8080`, ensure validators are configured, and upload
`contracts/EvidenceQuorumResolver.py` through **Contracts → Add From File**.
Deploy with no constructor arguments. Call `resolve` with a claim, criteria,
and a JSON string containing 2–5 HTTPS URLs.

To run the automated localnet test while Studio is running:

```powershell
$env:RUN_STUDIO_TESTS="1"
gltest tests/integration -v -s --network localnet
```

On macOS/Linux use `RUN_STUDIO_TESTS=1 gltest ...`.

Hosted Studio can be used without Docker at
[studio.genlayer.com](https://studio.genlayer.com). Upload the same single
contract file, or run `gltest ... --network studionet`.

## Contract API

### `resolve(claim, criteria, sources_json) -> str`

Creates and returns a numeric string ID. Inputs are bounded to control cost:
claim 10–1000 chars, criteria 10–1500 chars, and 2–5 unique HTTPS URLs.
Possible outcomes are `SUPPORTED`, `CONTRADICTED`, and `INCONCLUSIVE`.

### `get_resolution(id) -> Resolution`

Returns the stored claim, criteria, canonical source list, decision counts,
confidence, evidence digest, rationale, requester, and resolution flag.

### `get_count() -> u256`

Returns the number of accepted resolutions.

## Deploy from the CLI

With localnet running:

```bash
genlayer deploy --contract contracts/EvidenceQuorumResolver.py
```

Use Studio for the easiest interaction and validator-log inspection. Before
production use, validate critical web sources and exact runtime behavior on the
target testnet; Studio does not perfectly reproduce every live-network detail.

## Publish to GitHub

1. Create an empty repository named `evidence-quorum-resolver` on GitHub.
2. From this project directory run:

```bash
git init
git add .
git commit -m "Build EvidenceQuorum Resolver primitive"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/evidence-quorum-resolver.git
git push -u origin main
```

3. Add the contract category, test output, architecture summary, and known
   limitations to the GenLayer builder submission. Do not market the outcome as
   legal truth; it is a consensus result under user-supplied evidence criteria.

## Design notes

The validator compares stable decision fields and permits bounded variation in
counts and confidence. It deliberately does not compare free-form rationale or
the evidence digest, which may vary across models. See
[`docs/consensus-design.md`](docs/consensus-design.md).

## License

MIT
