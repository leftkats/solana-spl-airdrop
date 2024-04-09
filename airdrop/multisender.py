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
    for i, _ in enumerate(lines):
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
        if stdout:
            status = 'success'
            file_to_write = log_file_succeed
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
        print("i: ", i)

    recipients.close()
    log_file_succeed.close()
    # We don't want to have an empty file.
    if os.path.getsize(logs_failed_path) == 0:
        os.remove(logs_failed_path)
    else:
        log_file_failed.close()


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
    print("logs: ", log_entry)
    print(json.dumps(
        log_entry,
        ensure_ascii=True),
        file=log_file,
        flush=True,
    )


multisend(token_address, recipients_path, day_key)
