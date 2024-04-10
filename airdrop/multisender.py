import os
import json
from datetime import datetime
from subprocess import PIPE, Popen

DAB_TOKEN_ADDRESS = 'BBfACm5eg8CWmcRmgcn1c2uzN1fGhvQ1b8iDR92uaQVT'
DEVNET_TOKEN_ADDRESS=''

recipients_path = 'airdrop/recipients.txt'
day_key = datetime.now().strftime("%Y-%m-%d")


def send(
    token_address: str,
    recipient_address: str,
    amount: str,
):
    command = f"spl-token transfer --fund-recipient --allow-unfunded-recipient \
                {token_address} \
                {amount} \
                {recipient_address}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    # Log entry
    if stdout:
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
        stdout,
        stderr,
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
    except FileNotFoundError:
        print('Paid addresses file not found!')
    return paid_addresses


def get_recipients():
    recipients_new = []
    with open(recipients_path, 'r+') as recipients:
        rows = recipients.readlines()
        for row in rows:
            recipient_address = row.strip().split(',')[0]
            amount = row.strip().split(',')[1]
            recipients_new.append({
                'address': recipient_address,
                'amount': amount
            })
    return recipients_new


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
        logs=stdout.decode('utf-8') if stdout else stderr.decode('utf-8')
    )
    print(log_entry)
    print(json.dumps(
        log_entry,
        ensure_ascii=True),
        file=log_file,
        flush=True,
    )


# Read data
paid = get_paid_addresses()
recipients = get_recipients()

# Create log files
logs_succeed_path, mode = f'airdrop/airdrop-{day_key}-logs-succeed.json', 'w+'
if os.path.exists(logs_succeed_path):
    mode = 'a+'
log_file_succeed = open(logs_succeed_path, mode)

logs_failed_path, mode = f'airdrop/airdrop-{day_key}-logs-failed.json', 'w+'
if os.path.exists(logs_failed_path):
    mode = 'a+'
log_file_failed = open(logs_failed_path, mode)

# Tranfer tokens to recipients
for recipient in recipients:
    if recipient['address'] in paid:
        print(f'Found an already paid address --> {recipient["address"]}')
        # We continue here, but if the array is too big we could just delete the current address
        continue
    # send(mainnet_token_address, recipient["address"], recipient['amount'])
