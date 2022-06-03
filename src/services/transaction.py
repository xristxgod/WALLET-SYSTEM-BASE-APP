from typing import List, Dict

from main.models import TransactionModel
from src.services.__init__ import User, UserData
from src.services.__init__ import Transaction, TransactionRepository
from src.utils.utils import UtilsTransaction


class AllTransactionsRepository:
    """Transactions repository - It is used to store transaction data. To avoid touching the database once again"""
    def __init__(self):
        self.transactions: List[Transaction] = AllTransactionsRepository.get_transactions()

    @staticmethod
    def get_transactions() -> List[Transaction]:
        return UtilsTransaction.packaging_transactions(
            transactions=TransactionModel.objects.all()
        )


all_transactions_repository = AllTransactionsRepository()
