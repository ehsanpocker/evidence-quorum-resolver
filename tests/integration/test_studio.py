import os
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_STUDIO_TESTS") != "1",
    reason="set RUN_STUDIO_TESTS=1 with GenLayer Studio running",
)


def test_deploy_and_initial_state():
    contract = get_contract_factory("EvidenceQuorumResolver").deploy(args=[])
    assert contract.get_count().call() == 0
    # Live evidence resolution is intentionally manual: URLs and LLM outputs vary.
    tx = contract.resolve(args=[
        "The IANA example domain is reserved for documentation.",
        "At least two independent authoritative sources must confirm the reservation.",
        '["https://www.iana.org/help/example-domains","https://www.rfc-editor.org/rfc/rfc2606"]',
    ]).transact(wait_interval=5, wait_retries=120)
    assert tx_execution_succeeded(tx)
    assert contract.get_count().call() == 1
