import os
import json
from datetime import datetime
from subprocess import run


class Airdrop:
    """
    The class initialize the spl-tokens cli
    devnet: bool = True
    """

    def __init__(self, devnet: bool = True):
        self.recipients_path = "airdrop/recipients.txt"
        self.day_key = datetime.now().strftime("%Y-%m-%d")

        self.config = self.get_config(devnet=devnet)
        # self.init_solana()

        self.recipients = self.get_recipients()
        self.paid = self.get_paid_addresses()

        self.log_file_succeed, self.log_file_failed = self.create_log_files()

    def get_config(
        self,
        devnet: bool = True,
    ):
        import yaml

        with open("config.yml", "r") as file:
            config = yaml.safe_load(file)

        config = config["devnet"] if devnet else config["mainnet"]
        return config

    def init_solana(self):
        config_subnet = ["solana", "config", "set", "--url", self.config["url"]]
        keypair_config = [
            "solana",
            "config",
            "set",
            "--keypair",
            self.config["keypair_path"],
        ]

        result = run(config_subnet, capture_output=True, text=True)
        print(result)
        if result.stdout:
            result = run(keypair_config, capture_output=True, text=True)
            print(result)

    def send(
        self,
        token_address: str,
        recipient_address: str,
        amount: str,
    ):
        command = [
            "spl-token",
            "transfer",
            "--fund-recipient",
            "--allow-unfunded-recipient",
            token_address,
            amount,
            recipient_address,
        ]

        result = run(command, capture_output=True, text=True)

        # Log entry
        if result.stdout:
            status = "success"
            file_to_write = self.log_file_succeed
            data = self.parse_stdout(result.stdout)
            self.write_paid(recipient_address, amount, data["signature"])
        else:
            status = "failed"
            file_to_write = self.log_file_failed

        self.writetolog(
            status,
            token_address,
            recipient_address,
            result.stdout,
            result.stderr,
            file_to_write,
        )

    def write_paid(
        self,
        recipient,
        amount,
        signature,
    ):
        with open("airdrop/paid.ndjson", "a+") as paid:
            paid_account = {
                "address": recipient,
                "amount": amount,
                "signature": signature,
            }
            print(json.dumps(paid_account, ensure_ascii=True), file=paid, flush=True)

    def get_paid_addresses(self):
        paid_addresses = []
        try:
            with open("airdrop/paid.ndjson", "r+") as paid:
                rows = paid.readlines()
                for row in rows:
                    row = json.loads(row)
                    paid_addresses.append(row["address"])
        except Exception:
            print("Paid addresses file not found or is empty!")
        return paid_addresses

    def get_recipients(self):
        """
        Read recipients csv and return dictionary
        """
        with open(self.recipients_path, "r+") as recipients:
            rows = recipients.readlines()
            for row in rows:
                recipient_address = row.strip().split(",")[0]
                amount = row.strip().split(",")[1]
                yield {"address": recipient_address, "amount": amount}

    def writetolog(
        self, status, token_address, recipient_address, stdout, stderr, log_file
    ):
        log_entry = dict(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=status,
            sender_addr=token_address,
            reciever_addr=recipient_address,
            logs=stdout if stdout else stderr,
        )
        # print(log_entry)
        print(
            json.dumps(log_entry, ensure_ascii=True),
            file=log_file,
            flush=True,
        )

    def create_log_files(self):
        # Ensure airdrop folder exists
        os.makedirs("airdrop", exist_ok=True)

        logs_succeed_path = f"airdrop/airdrop-{self.day_key}-logs-succeed.json"
        mode = "a+" if os.path.exists(logs_succeed_path) else "w+"
        log_file_succeed = open(logs_succeed_path, mode)

        logs_failed_path = f"airdrop/airdrop-{self.day_key}-logs-failed.json"
        mode = "a+" if os.path.exists(logs_failed_path) else "w+"
        log_file_failed = open(logs_failed_path, mode)

        return log_file_succeed, log_file_failed

    def parse_stdout(
        self,
        stdout: str,
    ):
        import re

        data = {}
        recipient_pattern = r"Recipient: (.+)"
        token_account_pattern = r"Recipient associated token account: (.+)"
        signature_pattern = r"Signature: (.+)"

        recipient_match = re.search(recipient_pattern, stdout)
        if recipient_match:
            data["recipient"] = recipient_match.group(1)

        # Extract recipient associated token account
        token_account_match = re.search(token_account_pattern, stdout)
        if token_account_match:
            data["recipient_associated_token_account"] = token_account_match.group(1)

        # Extract signature
        signature_match = re.search(signature_pattern, stdout)
        if signature_match:
            data["signature"] = signature_match.group(1)
        return data


def multisend():
    airdrop = Airdrop()
    # Tranfer tokens to recipients
    for recipient in airdrop.get_recipients():
        if recipient["address"] in airdrop.paid:
            print(f"Found an already paid address --> {recipient['address']}")
            # We continue here, but if the array is too big we could just
            # delete the current address
            continue
        airdrop.send(
            airdrop.config["token_address"], recipient["address"], recipient["amount"]
        )
