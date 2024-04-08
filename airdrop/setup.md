## Prerequisites
- Prerequisite 1: Rust
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

## Setup commands spl-token-cli
```bash
# Install spl-token-cli
cargo install spl-token-cli
# Setup devnet env
solana config set --url https://api.devnet.solana.com
# Generate and config a test key
solana-keygen new --outfile ~/.config/solana/devnet.json
solana config set --keypair ~/.config/solana/devnet.json

# Check address
spl-token address
# Check account balances
spl-token accounts

# Create a token
spl-token create-token # Save the output
spl-token create-account <ADDR>
# Mint tokens
spl-token mint <ADDR> 1000000
# Transfer tokens
spl-token transfer <RECIPIENT_ADDR> 50000 <RECEIVER_ADDR> --fund-recipient

```