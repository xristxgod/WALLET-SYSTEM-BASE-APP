from typing import List, Dict

from src.services.__init__ import User, UserData, Transaction


class AllTransactionsRepository:
    """Transactions repository - It is used to store transaction data. To avoid touching the database once again"""
    def __init__(self, transactions: List[Dict]):
        self.transactions: List[Transaction] = ""