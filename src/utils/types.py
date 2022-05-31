from typing import Union

TG_CHAT_ID = Union[int, str, bytes]  # Telegram user id
TG_USERNAME = str  # Telegram user username

CRYPRO_ADDRESS = str  # Crypto wallet address

FULL_NETWORK = str  # Full network, External: TRON-TRX, TRON-USDT
NETWORK = str  # Network, External: TRON


class CoinsHelper(object):
    TRON = "TRX"

    @staticmethod
    def get_native_by_network(network: NETWORK) -> str:
        return CoinsHelper.__dict__.get(network.upper())