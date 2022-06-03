from typing import Optional, List
from dataclasses import dataclass

from src.utils.types import CRYPTO_TRANSACTION_HASH, CRYPTO_ADDRESS
from src.utils.types import TELEGRAM_USER_ID


class TransactionRepository:
    def reconnect(self):
        raise NotImplementedError

    @property
    def get_status(self):
        raise NotImplementedError



@dataclass
class Transaction:
    time: int
    transaction_hash: CRYPTO_TRANSACTION_HASH
    inputs: List[CRYPTO_ADDRESS]
    outputs: List[CRYPTO_ADDRESS]
    amount: float
    fee: Optional[float]
    status: Optional[int]


@dataclass
class UserData:
    chat_id: Optional[TELEGRAM_USER_ID]
    transactions: Optional[List[Transaction]]


@dataclass
class User:
    user_id: int
    data: Optional[List[UserData]]
