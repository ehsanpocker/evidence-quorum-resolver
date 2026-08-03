import json


CONTRACT = "contracts/EvidenceQuorumResolver.py"
SDK = "v0.2.12"
SOURCES = '["https://source-a.test/report","https://source-b.test/report"]'


def _answer(outcome="SUPPORTED", support=2, contradict=0, usable=2, confidence=90):
    return json.dumps({
        "outcome": outcome, "support_count": support,
        "contradict_count": contradict, "usable_source_count": usable,
        "confidence": confidence, "evidence_digest": "a" * 64,
        "rationale": "Both independent reports confirm the event."
    })


def test_resolution_persists_consensus_result(direct_vm, direct_deploy):
    direct_vm.mock_web(r"source-.*\.test/report", {"status": 200, "body": "Official result confirms launch."})
    direct_vm.mock_llm(r"evidence resolution engine", _answer())
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    resolution_id = resolver.resolve(
        "Project Alpha launched version 1.0 before July 2026.",
        "Supported only if two independent public sources confirm release and date.",
        SOURCES,
    )
    result = resolver.get_resolution(resolution_id)
    assert result.outcome == "SUPPORTED"
    assert result.support_count == 2
    assert resolver.get_count() == 1


def test_validator_accepts_close_independent_result(direct_vm, direct_deploy):
    direct_vm.mock_web(r"source-.*\.test/report", {"status": 200, "body": "Confirmed."})
    direct_vm.mock_llm(r"evidence resolution engine", _answer(confidence=90))
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    resolver.resolve("A claim long enough to evaluate", "Two independent confirmations are required", SOURCES)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"source-.*\.test/report", {"status": 200, "body": "Confirmed independently."})
    direct_vm.mock_llm(r"evidence resolution engine", _answer(confidence=78))
    assert direct_vm.run_validator() is True


def test_validator_rejects_opposite_outcome(direct_vm, direct_deploy):
    direct_vm.mock_web(r"source-.*\.test/report", {"status": 200, "body": "Confirmed."})
    direct_vm.mock_llm(r"evidence resolution engine", _answer())
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    resolver.resolve("A claim long enough to evaluate", "Two independent confirmations are required", SOURCES)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"source-.*\.test/report", {"status": 200, "body": "Denied."})
    direct_vm.mock_llm(r"evidence resolution engine", _answer("CONTRADICTED", 0, 2, 2, 90))
    assert direct_vm.run_validator() is False
