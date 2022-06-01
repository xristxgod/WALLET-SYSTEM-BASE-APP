from src.utils.types import NETWORK

class CryptoService:

    def __init__(self, network: NETWORK):
        self.__network = network

    @property
    def network(self) -> NETWORK:
        return self.__network

    def create_wallet(self):
        pass

    def get_balance(self):
        pass

    def get_optimal_fee(self):
        pass

TRON = CryptoService(network="TRON")