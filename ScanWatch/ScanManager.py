from tqdm import tqdm

from ScanWatch.Client import Client
from ScanWatch.storage.ScanDataBase import ScanDataBase
from ScanWatch.utils.enums import NETWORK, TRANSACTION


class ScanManager:
    """
    This class is the interface between the user, the API and the Database
    """

    def __init__(self, address: str, nt_type: NETWORK, api_token: str):
        """
        Initiate the manager

        :param address: address to monitor
        :type address: str
        :param nt_type: type of the network
        :type nt_type: NETWORK
        :param api_token: token to communicate with the API
        :type api_token: str
        """
        self.address = address
        self.nt_type = nt_type
        self.client = Client(api_token, self.nt_type)
        self.db = ScanDataBase()

    def update_transactions(self, tr_type: TRANSACTION):
        """
        Update the transactions of a certain type in the database

        :param tr_type: type of transaction to update
        :type tr_type: TRANSACTION
        :return: None
        :rtype: None
        """
        last_block = self.db.get_last_block_number(self.address, self.nt_type, tr_type)
        if tr_type == TRANSACTION.NORMAL:
            new_transactions = self.client.get_normal_transactions(self.address, start_block=last_block + 1)
        elif tr_type == TRANSACTION.INTERNAL:
            new_transactions = self.client.get_internal_transactions(self.address, start_block=last_block + 1)
        elif tr_type == TRANSACTION.ERC20:
            new_transactions = self.client.get_erc20_transactions(self.address, start_block=last_block + 1)
        elif tr_type == TRANSACTION.ERC721:
            new_transactions = self.client.get_erc721_transactions(self.address, start_block=last_block + 1)
        else:
            raise ValueError(f"unknown transaction type: {tr_type}")
        self.db.add_transactions(self.address, self.nt_type, tr_type, new_transactions)

    def update_all_transactions(self):
        """
        Update all the transactions for the address

        :return: None
        :rtype: None
        """
        tr_types_names = [name for name in dir(TRANSACTION) if not name.startswith('__')]
        pbar = tqdm(total=len(tr_types_names))
        for name in tr_types_names:
            pbar.set_description(f"fetching {name.lower()} transactions for {self.nt_type.name.lower()} "
                                 f"address {self.address[:5]}...{self.address[-5:]}")
            self.update_transactions(getattr(TRANSACTION, name))
            pbar.update()
        pbar.set_description(f"all transactions updated for address {self.address[:5]}...{self.address[-5:]}")
        pbar.close()

    def get_transactions(self, tr_type: TRANSACTION):
        """
        Return the transactions of the provided type that are saved locally for the address of the manager

        :param tr_type: type of transaction to fetch
        :type tr_type: TRANSACTION
        :return: list of transactions
        :rtype: List[Dict]
        """
        return self.db.get_transactions(self.address, self.nt_type, tr_type)
