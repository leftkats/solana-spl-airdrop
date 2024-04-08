import os
import json
from datetime import datetime
from subprocess import PIPE, Popen

recipients_filename = 'recipients.txt'
token_address = '39dyZi6jX9ZWPqjT2td33UQYKa4gcCbqDy5MjQPVRsEC'
amount = 10

day_key = datetime.now().strftime("%Y-%m-%d")

logs_filename, mode = f'airdrop-{day_key}.logs', 'w+'
if os.path.exists(logs_filename):
    mode = 'a+'
log_file = open(logs_filename, mode)

recipients = open('/Users/elef/github/telon/solana-airdrop/recipients.txt', 'r+')
lines = recipients.readlines()

for i, line in enumerate(lines):
    recipient_address = lines[i].strip()
    command = f"spl-token transfer --fund-recipient \
                {token_address} \
                {amount} \
                {recipient_address}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender_addr": token_address,
        "reciever_addr": recipient_address,
        "logs": stdout.decode('utf-8') if stdout else stderr.decode('utf-8')
    }
    json.dump(log_entry, log_file, ensure_ascii=True)
    log_file.write('\n')
