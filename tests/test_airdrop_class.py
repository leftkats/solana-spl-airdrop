import json
import os
import pytest
from unittest.mock import patch, MagicMock
from src.airdrop import Airdrop


@pytest.fixture
def setup_test_files(tmp_path):
    # Create config.yml
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        """
devnet:
  url: "https://api.devnet.solana.com"
  keypair_path: "test-keypair.json"
  token_address: "FakeTokenAddress123"
"""
    )

    # Create recipients.txt
    recipients_dir = tmp_path / "airdrop"
    recipients_dir.mkdir()
    recipients_file = recipients_dir / "recipients.txt"
    recipients_file.write_text("recipient1,10\nrecipient2,20\n")

    # Empty paid.ndjson
    paid_file = recipients_dir / "paid.ndjson"
    paid_file.write_text("")

    return {
        "base_dir": tmp_path,
        "recipients_file": recipients_file,
        "paid_file": paid_file,
        "config_file": config_path,
    }


@pytest.fixture
def patch_env(monkeypatch, setup_test_files):
    # Change working directory so config.yml can be found
    monkeypatch.chdir(setup_test_files["base_dir"])
    return setup_test_files


def test_get_config(patch_env):
    airdrop = Airdrop(devnet=True)
    assert isinstance(airdrop.config, dict)
    assert "url" in airdrop.config
    assert airdrop.config["url"] == "https://api.devnet.solana.com"


def test_get_recipients(patch_env):
    airdrop = Airdrop(devnet=True)
    recipients = list(airdrop.get_recipients())
    assert len(recipients) == 2
    assert recipients[0]["address"] == "recipient1"
    assert recipients[0]["amount"] == "10"


@patch("src.airdrop.run")
def test_send_success(mock_run, patch_env):
    stdout = (
        "Recipient: recipient1\n"
        "Recipient associated token account: TokenAcct123\n"
        "Signature: SignatureXYZ123\n"
    )
    mock_run.return_value.stdout = stdout
    mock_run.return_value.stderr = ""

    airdrop = Airdrop(devnet=True)
    airdrop.send(
        token_address=airdrop.config["token_address"],
        recipient_address="recipient1",
        amount="10",
    )

    paid_path = patch_env["paid_file"]
    assert paid_path.exists()
    lines = paid_path.read_text().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["address"] == "recipient1"
    assert entry["signature"] == "SignatureXYZ123"
