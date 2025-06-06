# ☀️🐍📄 Solana SPL Token Airdrop Script

[![Solana](https://img.shields.io/badge/Solana-%23000000.svg?style=for-the-badge&logo=solana&logoColor=white)](https://solana.com/) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![PyYAML](https://img.shields.io/badge/PyYAML-%230077BE.svg?style=for-the-badge&logo=PyYAML&logoColor=white)](https://pyyaml.org/)

# Solana SPL Token Airdrop Script

This Python script automates the process of airdropping SPL tokens to a list of recipients on the Solana blockchain. It utilizes the `spl-token` CLI and logs transaction details.

## Description

The `Airdrop` class manages the distribution of SPL tokens. It reads recipient addresses and amounts from a `recipients.txt` file, sends the tokens using the `spl-token` CLI, and logs the results. It supports both devnet and mainnet configurations through a `config.yml` file. It also tracks already paid addresses to prevent duplicate transactions.

## Features

-   **Configuration:** Supports devnet and mainnet configurations via `config.yml`.
-   **Recipient Management:** Reads recipient addresses and amounts from `airdrop/recipients.txt`.
-   **Transaction Logging:** Logs successful and failed transactions in separate JSON files.
-   **Paid Address Tracking:** Prevents duplicate transactions by tracking already paid addresses in `airdrop/paid.ndjson`.
-   **Error Handling:** Logs errors and provides detailed output for debugging.
-   **Solana CLI Integration:** Utilizes the `spl-token` CLI for token transfers.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Install dependencies:**

    Ensure you have Python 3.6+ installed.

    ```bash
    pip install pyyaml
    ```

3.  **Install Solana CLI:**

    Follow the official Solana CLI installation instructions: [Solana CLI Installation](https://docs.solana.com/cli/install)

4.  **Configure Solana CLI:**

    Run `solana config set --url <your_rpc_url>` and `solana config set --keypair <your_keypair_path>` to configure your Solana CLI.

5.  **Configure `config.yml`:**

    Create a `config.yml` file in the root directory with the following structure:

    ```yaml
    devnet:
      url: "[https://api.devnet.solana.com](https://api.devnet.solana.com)"
      keypair_path: "/path/to/your/devnet.json"
      token_address: "your_devnet_token_address"
    mainnet:
      url: "[https://api.mainnet-beta.solana.com](https://api.mainnet-beta.solana.com)"
      keypair_path: "/path/to/your/mainnet.json"
      token_address: "your_mainnet_token_address"
    ```

    Replace placeholders with your actual values.

6.  **Create `airdrop/recipients.txt`:**

    Create a `airdrop/recipients.txt` file with recipient addresses and amounts, one per line, separated by a comma:

    ```
    recipient_address_1,amount_1
    recipient_address_2,amount_2
    ...
    ```

## Usage

1.  **Run the script:**

    ```bash
    python your_script_name.py
    ```

    The script will read the `recipients.txt` file and airdrop tokens to each recipient.

2.  **Devnet or Mainnet:**
    The script defaults to devnet. If you want to use mainnet, change the first line of the multisend() function to `airdrop = Airdrop(devnet=False)`

## Files

-   `config.yml`: Configuration file for Solana network and keypair settings.
-   `airdrop/recipients.txt`: List of recipient addresses and amounts.
-   `airdrop/paid.ndjson`: Log of paid addresses and transaction signatures.
-   `airdrop/airdrop-<YYYY-MM-DD>-logs-succeed.json`: Log of successful transactions.
-   `airdrop/airdrop-<YYYY-MM-DD>-logs-failed.json`: Log of failed transactions.


### Wall of Contributors
<a href="https://github.com/leftkats/solana-spl-airdrop/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=leftkats/solana-spl-airdrop" />
</a>

If you like the repo please support with a :star:

Thank you for being here!