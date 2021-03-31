from typing import Dict, Optional

import requests


class Client:
    """
    Client for the etherscan.io API
    https://etherscan.io/apis
    """
    BASE_URL = "https://api.etherscan.io/api"

    def __init__(self, api_token: str):
        self.api_token = api_token

    def get_erc721_transactions(self, address: str, start_block: Optional[int] = None, end_block: Optional[int] = None):
        """
        fetch erc721 transactions on an eth address

        :param address: ETH address
        :type address: str
        :param start_block: fetch transactions starting with this block
        :type start_block: Optional[int]
        :param end_block: fetch transactions until this block
        :type end_block: Optional[int]
        :return: List of transactions
        :rtype: List[Dict]
        """
        return self._get_transactions(address, 'tokennfttx', start_block, end_block)

    def get_erc20_transactions(self, address: str, start_block: Optional[int] = None, end_block: Optional[int] = None):
        """
        fetch erc20 transactions on an eth address

        :param address: ETH address
        :type address: str
        :param start_block: fetch transactions starting with this block
        :type start_block: Optional[int]
        :param end_block: fetch transactions until this block
        :type end_block: Optional[int]
        :return: List of transactions
        :rtype: List[Dict]

        .. code-block:: python

            [{'blockNumber': '108941',
              'timeStamp': '148216518',
              'hash': '0948461czecc9ze8e4vsvbq94sd96',
              'nonce': '23908745',
              'blockHash': '0x74a984dz56c13v8ze9q451vda',
              'from': 'zazd9f1wsqda84zds5qd6zda',
              'contractAddress': 'azd984f1edazdadqfefa',
              'to': '84cazd984csgzefa984zq5s1c',
              'value': '15248960000000000000',
              'tokenName': 'ChainLink Token',
              'tokenSymbol': 'LINK',
              'tokenDecimal': '18',
              'transactionIndex': '45',
              'gas': '200001',
              'gasPrice': '100000000000',
              'gasUsed': '51481',
              'cumulativeGasUsed': '1491504',
              'input': 'deprecated',
              'confirmations': '1948513'},
            ...
            ]

        """
        return self._get_transactions(address, 'tokentx', start_block, end_block)

    def get_normal_transactions(self, address: str, start_block: Optional[int] = None, end_block: Optional[int] = None):
        """
        fetch normal transactions on an eth address

        :param address: ETH address
        :type address: str
        :param start_block: fetch transactions starting with this block
        :type start_block: Optional[int]
        :param end_block: fetch transactions until this block
        :type end_block: Optional[int]
        :return: List of transactions
        :rtype: List[Dict]

        .. code-block:: python

            [{'blockNumber': '10272495',
              'timeStamp': '1485965131',
              'hash': 'd9azfv1q9zf84zr15f49f49zef1z3sd1g98t1b6',
              'nonce': '9846651',
              'blockHash': 'zad94v16s1qef9a4f9v1r53b1sq64daf',
              'from': '496a1ef65s1dbv4a96z513svez965q',
              'contractAddress': 'az41f8ze1f63q5s1gv89ez49',
              'to': 'az49f84161ac89s4ef984a96e',
              'value': '17854000000000000000',
              'tokenName': 'ChainLink Token',
              'tokenSymbol': 'LINK',
              'tokenDecimal': '18',
              'transactionIndex': '79',
              'gas': '200001',
              'gasPrice': '100000000000',
              'gasUsed': '84215',
              'cumulativeGasUsed': '1531404',
              'input': 'deprecated',
              'confirmations': '119452'},
            ...
            ]
        """
        return self._get_transactions(address, 'txlist', start_block, end_block)

    def get_internal_transactions(self, address: str, start_block: Optional[int] = None,
                                  end_block: Optional[int] = None):
        """
        fetch internal transactions on an eth address

        :param address: ETH address
        :type address: str
        :param start_block: fetch transactions starting with this block
        :type start_block: Optional[int]
        :param end_block: fetch transactions until this block
        :type end_block: Optional[int]
        :return: List of transactions
        :rtype: List[Dict]
        """
        return self._get_transactions(address, 'txlistinternal', start_block, end_block)

    def _get_transactions(self, address: str, action: str, start_block: Optional[int] = None,
                          end_block: Optional[int] = None):
        """
        fetch transactions on an eth address

        :param address: ETH address
        :type address: str
        :param action: name of the request for the api (ex 'txlist' or 'txlistinternal')
        :type action:
        :param start_block: fetch transactions starting with this block
        :type start_block: Optional[int]
        :param end_block: fetch transactions until this block
        :type end_block: Optional[int]
        :return: List of transactions
        :rtype: List[Dict]
        """
        offset = 10000
        page_number = 1
        transactions = []
        while True:
            url = self.get_url_request(module='account',
                                       action=action,
                                       sort='asc',
                                       address=address,
                                       start_block=start_block,
                                       end_block=end_block,
                                       page=page_number,
                                       offset=offset)
            batch_txs = self.get_result(url)
            transactions.extend(batch_txs)
            if len(batch_txs) < offset:
                break
            else:
                page_number += 1
        return transactions

    def get_balance(self, address: str) -> float:
        """
        fetch the current eth balance of an address

        :param address: ETH address
        :type address: str
        :return: ETH amount
        :rtype: float
        """
        url = self.get_url_request(module='account',
                                   action='balance',
                                   address=address,
                                   tag='latest'
                                   )
        return float(self.get_result(url))

    def get_url_request(self, **kwargs) -> str:
        """
        Construct the url to make a request to the etherscan.io API

        :param kwargs: keywords args for the endpoint
        :type kwargs: Any
        :return:
        :rtype:
        """
        _keywords = {**kwargs, "apikey": self.api_token}
        string_kws = "&".join((f"{key}={value}" for key, value in _keywords.items()))
        return f"{Client.BASE_URL}?{string_kws}"

    @staticmethod
    def get_result(url: str):
        """
        call the API with an url, raise if the status is not ok and return the API result

        :param url: url to request for the etherscan.io
        :type url: str
        :return: API result
        :rtype: depend of the endpoint
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['result']
