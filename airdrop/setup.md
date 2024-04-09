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

## Setup main net
```bash
solana config set --url https://api.mainnet-beta.solana.com/
# Create wallet
solana-keygen new --outfile ~/.config/solana/mainnet.json
# Config the new wallet
solana config set --keypair ~/.config/solana/mainnet.json
# Create token address
spl-token address --token BBfACm5eg8CWmcRmgcn1c2uzN1fGhvQ1b8iDR92uaQVT --verbose
```