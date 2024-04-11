import os
import json
from datetime import datetime
from subprocess import run


def get_config(
    devnet: bool = False,
):
    import yaml
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    config = config['devnet'] if devnet else config['mainnet']
    return config


def init_solana(config: dict):
    config_subnet = ['solana', 'config', 'set', '--url', config['url']]
    keypair_config = ['solana', 'config', 'set', '--keypair', config['keypair_path']]

    result = run(config_subnet, capture_output=True, text=True)
    if result.stdout:
        result = run(keypair_config, capture_output=True, text=True)


def send(
    token_address: str,
    recipient_address: str,
    amount: str,
):
    command = ['spl-token', 'transfer', '--fund-recipient', '--allow-unfunded-recipient', token_address, amount, recipient_address]
    result = run(command, capture_output=True, text=True)
    # Log entry
    if result.stdout:
        status = 'success'
        file_to_write = log_file_succeed
        write_paid(recipient_address, amount, 'signature')
    else:
        status = 'failed'
        file_to_write = log_file_failed

    writetolog(
        status,
        token_address,
        recipient_address,
        result.stdout,
        result.stderr,
        file_to_write,
    )


def write_paid(recipient, amount, signature):
    with open('airdrop/paid.ndjson', 'a+') as paid:
        paid_account = {
            "address": recipient,
            "amount": amount,
            "signature": "xx"
        }
        print(json.dumps(paid_account, ensure_ascii=True), file=paid, flush=True)


def get_paid_addresses():
    paid_addresses = []
    try:
        with open('airdrop/paid.ndjson', 'r+') as paid:
            rows = paid.readlines()
            for row in rows:
                row = json.loads(row)
                paid_addresses.append(row['address'])
    except Exception:
        print('Paid addresses file not found or is empty!')
    return paid_addresses


def get_recipients():
    """
    Read recipients csv and return dictionary
    """
    with open(recipients_path, 'r+') as recipients:
        rows = recipients.readlines()
        for row in rows:
            recipient_address = row.strip().split(',')[0]
            amount = row.strip().split(',')[1]
            yield {
                'address': recipient_address,
                'amount': amount
            }


def writetolog(
    status,
    token_address,
    recipient_address,
    stdout,
    stderr,
    log_file
):
    log_entry = dict(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=status,
        sender_addr=token_address,
        reciever_addr=recipient_address,
        logs=stdout if stdout else stderr
    )
    # print(log_entry)
    print(json.dumps(
        log_entry,
        ensure_ascii=True),
        file=log_file,
        flush=True,
    )


def create_log_files():
    # Create log files
    logs_succeed_path = f'airdrop/airdrop-{day_key}-logs-succeed.json'
    mode = 'a+' if os.path.exists(logs_succeed_path) else 'w+'
    log_file_succeed = open(logs_succeed_path, mode)

    logs_failed_path = f'airdrop/airdrop-{day_key}-logs-failed.json'
    mode = 'a+' if os.path.exists(logs_failed_path) else 'w+'
    log_file_failed = open(logs_failed_path, mode)

    return log_file_succeed, log_file_failed


# Config
recipients_path = 'airdrop/recipients.txt'
day_key = datetime.now().strftime("%Y-%m-%d")
config = get_config(devnet=True)
init_solana(config)

# Read data
paid = get_paid_addresses()

log_file_succeed, log_file_failed = create_log_files()

# Tranfer tokens to recipients
for recipient in get_recipients():
    if recipient['address'] in paid:
        print(f'Found an already paid address --> {recipient["address"]}')
        # We continue here, but if the array is too big we could just delete the current address
        continue
    send(config['token_address'], recipient["address"], recipient['amount'])
