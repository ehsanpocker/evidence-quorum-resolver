# Step-by-step setup

## 1. Install tools

Install Git, Python 3.12+, and optionally VS Code. For local Studio also install
Node.js 18+, Docker Desktop 26+, and ensure Docker is running.

## 2. Prepare Python

Create a virtual environment, activate it, upgrade pip, and install
`requirements.txt`. Run the linter, then Direct Mode tests. These tests need no
Docker or network and exercise storage, input bounds, and validator agreement.

## 3. Start localnet

Install the CLI with `npm install -g genlayer`, run `genlayer init
--numValidators 5`, then `genlayer up --numValidators 5`. Studio opens at
`http://localhost:8080`; RPC is `http://localhost:4000/api`.

## 4. Interactive Studio test

Upload the contract file, deploy with no arguments, and invoke `resolve`. Pass
the source list as one JSON string, for example:

```json
["https://www.iana.org/help/example-domains","https://www.rfc-editor.org/rfc/rfc2606"]
```

Wait for consensus, then call `get_count` and `get_resolution("1")`. Inspect
leader and validator logs to confirm every node fetched evidence independently.

## 5. Automated integration test

Set `RUN_STUDIO_TESTS=1` and run `gltest tests/integration -v -s --network
localnet`. Live web/LLM behavior can be slow or temporarily inconclusive, so this
test is opt-in and Direct Mode remains the deterministic CI gate.

## 6. Publish

Create an empty GitHub repository, initialize Git locally, commit all files, set
the remote, and push `main`. Add CI only after pinning dependency versions known
to work in your environment. Never commit `.env` or account private keys.
