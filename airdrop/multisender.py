import os
import json
from datetime import datetime
from subprocess import PIPE, Popen

token_address = '39dyZi6jX9ZWPqjT2td33UQYKa4gcCbqDy5MjQPVRsEC'
recipients_path = 'airdrop/recipients.txt'
day_key = datetime.now().strftime("%Y-%m-%d")


def multisend(
    token_address: str,
    recipients_path: str,
    day_key: datetime,
):
    logs_succeed_path, mode = f'airdrop/airdrop-{day_key}-logs-succeed.json', 'w+'
    if os.path.exists(logs_succeed_path):
        mode = 'a+'
    log_file_succeed = open(logs_succeed_path, mode)

    logs_failed_path, mode = f'airdrop/airdrop-{day_key}-logs-failed.json', 'w+'
    if os.path.exists(logs_failed_path):
        mode = 'a+'
    log_file_failed = open(logs_failed_path, mode)


    recipients = open(recipients_path, 'r+')
    lines = recipients.readlines()
    for i, line in enumerate(lines):
        # Transfer
        recipient_address = lines[i].strip().split(',')[0]
        amount = lines[i].strip().split(',')[1]

        command = f"spl-token transfer --fund-recipient \
                    {token_address} \
                    {amount} \
                    {recipient_address}"
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # Log entry
        status = 'success' if stdout else 'failed'
        log_entry = dict(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=status,
            sender_addr=token_address,
            reciever_addr=recipient_address,
            logs=stdout.decode('utf-8') if stdout else stderr.decode('utf-8')
        )
        print(json.dumps(
            log_entry,
            ensure_ascii=True),
            file=log_file_succeed,
            flush=True,
        )

    recipients.close()
    log_file_succeed.close()
    # We don't want to have an empty file.
    if os.path.getsize(logs_failed_path) == 0:
        os.remove(logs_failed_path)


multisend(token_address, recipients_path, day_key)
