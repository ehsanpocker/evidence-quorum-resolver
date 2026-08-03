import pytest


CONTRACT = "contracts/EvidenceQuorumResolver.py"
SDK = "v0.2.12"


def test_initial_state(direct_deploy):
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    assert resolver.get_count() == 0


def test_rejects_too_few_sources(direct_deploy):
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    with pytest.raises(Exception, match="2..5"):
        resolver.resolve("A sufficiently long claim", "Clear resolution criteria", '["https://example.com"]')


def test_rejects_non_https_and_duplicates(direct_deploy):
    resolver = direct_deploy(CONTRACT, sdk_version=SDK)
    with pytest.raises(Exception, match="HTTPS"):
        resolver.resolve("A sufficiently long claim", "Clear resolution criteria", '["http://a.test","https://b.test"]')
    with pytest.raises(Exception, match="duplicate"):
        resolver.resolve("A sufficiently long claim", "Clear resolution criteria", '["https://a.test","https://a.test"]')
