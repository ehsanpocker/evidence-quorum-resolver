# Test report

Validated on 2026-08-03 with Python 3.13.7 and `genlayer-test` 0.29.2.

## Completed

- Test discovery succeeds: 6 Direct Mode tests are collected.
- The current `gltest.config.yaml` is accepted by `genlayer-test` 0.29.2.
- Python syntax compilation passes for contract and test sources.
- Direct tests cover initialization, input rejection, accepted settlement,
  bounded validator disagreement, and rejection of the opposite outcome.

## Environment limitation

The first Direct Mode attempt reached the official runner but
`genlayer-test` auto-selected GenVM `v0.3.0-rc7`; its expected
`genvm-universal.tar.xz` URL returned HTTP 404. Tests are now explicitly pinned
to the stable fallback `v0.2.12`. The follow-up SDK cache download could not be
authorized in this build environment, so a green runtime result is not claimed.

Run `pytest tests/direct -v` in a normal environment with network access. If
the pinned SDK is already cached, no download is required. Studio integration
was not run because no local GenLayer Studio instance was available.
