class SolanaDummyClient:
    """
    A dummy client to simulate interaction with the Solana blockchain.
    Useful for testing structure, not functionality.
    """

    def __init__(self, network: str = "devnet"):
        self.network = network
        self.endpoint = self._get_endpoint(network)

    def _get_endpoint(self, network: str) -> str:
        if network == "devnet":
            return "https://api.devnet.solana.com"
        elif network == "mainnet":
            return "https://api.mainnet-beta.solana.com"
        else:
            return "https://api.testnet.solana.com"

    def get_balance(self, address: str) -> int:
        """
        Simulate returning a fixed balance for an address.
        """
        return 1000000000  # dummy lamports

    def send_dummy_transaction(self, sender: str, recipient: str, amount: int) -> str:
        """
        Pretend to send a transaction and return a fake signature.
        """
        return "5YdUmMySigNatuRd2xE1234567890abcdefg"
