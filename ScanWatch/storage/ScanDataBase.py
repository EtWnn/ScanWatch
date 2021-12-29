from typing import Dict, List

from ScanWatch.storage.DataBase import DataBase
from ScanWatch.storage.tables import get_transaction_table
from ScanWatch.utils.enums import TRANSACTION, NETWORK


class ScanDataBase(DataBase):
    """
    Handles the recording of the address transactions in a local database
    """

    def __init__(self, name: str = 'scan_db'):
        """
        Initialise a Scan database instance

        :param name: name of the database
        :type name: str
        """
        super().__init__(name)

    def add_transactions(self, address: str, nt_type: NETWORK, net: str, tr_type: TRANSACTION, transactions: List[Dict]):
        """
        Add a list of transactions to the database

        :param address: address involved in the transaction
        :type address: str
        :param nt_type: type of network
        :type nt_type: NETWORK
        :param net: name of the network, used to differentiate main and test nets
        :type net: str
        :param tr_type: type of the transaction to record
        :type tr_type: TRANSACTION
        :param transactions: list of the transaction to record
        :type transactions: List[Dict]
        :return: None
        :rtype: None
        """
        table = get_transaction_table(address, nt_type, net, tr_type)
        for transaction in transactions:
            row = table.dict_to_tuple(transaction)
            self.add_row(table, row, auto_commit=False)
        self.commit()

    def get_transactions(self, address: str, nt_type: NETWORK, net: str, tr_type: TRANSACTION) -> List[Dict]:
        """
        Return the List of the transactions recorded in the database

        :param address: address involved in the transactions
        :type address: str
        :param nt_type: type of network
        :type nt_type: NETWORK
        :param net: name of the network, used to differentiate main and test nets
        :type net: str
        :param tr_type: type of the transaction to fetch
        :type tr_type: TRANSACTION
        :return: list of the transaction recorded
        :rtype: List[Dict]
        """
        table = get_transaction_table(address, nt_type, net, tr_type)
        rows = self.get_all_rows(table)
        return [table.tuple_to_dict(row) for row in rows]

    def get_last_block_number(self, address: str, nt_type: NETWORK, net: str, tr_type: TRANSACTION) -> int:
        """
        Return the last block number seen in recorded transactions (per address, type of transaction and network)
        If None are found, return 0

        :param address: address involved in the transactions
        :type address: str
        :param nt_type: type of network
        :type nt_type: NETWORK
        :param net: name of the network, used to differentiate main and test nets
        :type net: str
        :param tr_type: type of the transaction to fetch
        :type tr_type: TRANSACTION
        :return: last block number
        :rtype: int
        """
        table = get_transaction_table(address, nt_type, net, tr_type)
        selection = str(table.blockNumber)
        query = self.get_conditions_rows(table, selection=selection)
        default = 0
        try:
            return max([int(e[0]) for e in query])
        except ValueError:
            return default



