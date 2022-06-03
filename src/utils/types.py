from typing import Optional

CRYPTO_NETWORK = str                   # Crypto network
CRYPTO_ADDRESS = str                   # Crypto wallet address
CRYPTO_MNEMONIC = str                  # Crypto wallet mnemonic phrase


class CoinHelper:
    TRON = "TRX"

    @staticmethod
    def get_native_coin(network: CRYPTO_NETWORK) -> Optional[str]:
        return CoinHelper.__dict__.get(network)