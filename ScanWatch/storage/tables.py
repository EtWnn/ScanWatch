from typing import List, Optional, Tuple, Dict

from ScanWatch.utils.enums import NETWORK, TRANSACTION


class Table:
    """
    This class represent a table in a database. All columns names are dynamic attributes
    @DynamicAttrs
    This class is used to describe the tables that will be used to in the database
    """

    def __init__(self, name: str, columns_names: List[str], columns_sql_types: List[str],
                 primary_key: Optional[str] = None, primary_key_sql_type: Optional[str] = None):
        """
        Initialise a Table instance

        :param name: name of the table
        :type name: str
        :param columns_names: names of the columns (except primary column)
        :type columns_names: List[str]
        :param columns_sql_types: sql types of the previous columns
        :type columns_sql_types: List[str]
        :param primary_key: name of the primary key (None, if no primary key is needed)
        :type primary_key: Optional[str]
        :param primary_key_sql_type: sql type of the primary key (None, if no primary key is needed)
        :type primary_key_sql_type: Optional[str]
        """
        self.name = name
        self.columns_names = columns_names
        self.columns_sql_types = columns_sql_types
        self.primary_key = primary_key
        self.primary_key_sql_type = primary_key_sql_type

        for column_name in self.columns_names:
            try:
                value = getattr(self, column_name)
                raise ValueError(f"the name {column_name} conflicts with an existing attribute of value {value}")
            except AttributeError:
                setattr(self, column_name, column_name)

        if self.primary_key is not None:
            setattr(self, self.primary_key, self.primary_key)

    def tuple_to_dict(self, row: Tuple) -> Dict:
        """
        Transform a row from Tuple to Dict with column names as keys.

        :param row: a row of this table
        :type row: Tuple
        :return: the dictionary equivalent of this row
        :rtype: Dict
        """
        keys = []
        if self.primary_key is not None:
            keys.append(self.primary_key)
        keys += self.columns_names
        if len(keys) != len(row):
            raise ValueError(f"{len(keys)} values were expected but the row submitted only has {len(row)}")
        return {k: v for k, v in zip(keys, row)}

    def dict_to_tuple(self, row: Dict) -> Tuple:
        """
        Transform a row from Dict to Tuple, in the order of the table columns

        :param row: a row of this table
        :type row: Dict
        :return: the tuple equivalent of this row
        :rtype: Tuple
        """
        keys = []
        if self.primary_key is not None:
            keys.append(self.primary_key)
        keys += self.columns_names
        try:
            return tuple([row[k] for k in keys])
        except KeyError:
            raise ValueError(f"missing keys in the row provided: {keys} are expected")


def get_normal_transaction_table(address: str, scan_type: NETWORK):
    """
    Return the table used to store the normal transactions for an address and a scan type

    :param address: address of the transactions
    :type address: str
    :param scan_type: scan type: ether or bsc
    :type scan_type: str
    :return: table to store the transactions
    :rtype: Table
    """
    rows = [
        'blockNumber',
        'timeStamp',
        'hash',
        'nonce',
        'blockHash',
        'transactionIndex',
        'from',
        'to',
        'value',
        'gas',
        'gasPrice',
        'isError',
        'txreceipt_status',
        'input',
        'contractAddress',
        'cumulativeGasUsed',
        'gasUsed',
        'confirmations',
    ]
    row_types = len(rows) * ['TEXT']
    return Table(f"{scan_type}_{address}_normal_transaction", rows, row_types)


def get_transaction_table(address: str, nt_type: NETWORK, tr_type: TRANSACTION):
    """
    Return the table used to store the transactions depending on the address, network type and transaction type

    :param address: address of the transactions
    :type address: str
    :param nt_type: type of network
    :type nt_type: NETWORK
    :param tr_type: type of the transaction to record
    :type tr_type: TRANSACTION
    :return: corresponding table
    :rtype: Table
    """
    if tr_type == TRANSACTION.NORMAL:
        rows = [
            'blockNumber',
            'timeStamp',
            'hash',
            'nonce',
            'blockHash',
            'transactionIndex',
            'from',
            'to',
            'value',
            'gas',
            'gasPrice',
            'isError',
            'txreceipt_status',
            'input',
            'contractAddress',
            'cumulativeGasUsed',
            'gasUsed',
            'confirmations',
        ]
    elif tr_type == TRANSACTION.ERC20:
        rows = [
            'blockNumber',
            'timeStamp',
            'hash',
            'nonce',
            'blockHash',
            'from',
            'contractAddress',
            'to',
            'value',
            'tokenName',
            'tokenSymbol',
            'tokenDecimal',
            'transactionIndex',
            'gas',
            'gasPrice',
            'gasUsed',
            'cumulativeGasUsed',
            'input',
            'confirmations',
        ]
    elif tr_type == TRANSACTION.ERC721:
        rows = [
            'blockNumber',
            'timeStamp',
            'hash',
            'nonce',
            'blockHash',
            'from',
            'contractAddress',
            'to',
            'tokenID',
            'tokenName',
            'tokenSymbol',
            'tokenDecimal',
            'transactionIndex',
            'gas',
            'gasPrice',
            'gasUsed',
            'cumulativeGasUsed',
            'input',
            'confirmations',
        ]
    elif tr_type == TRANSACTION.INTERNAL:
        rows = [
            'blockNumber',
            'timeStamp',
            'hash',
            'from',
            'to',
            'value',
            'contractAddress',
            'input',
            'type',
            'gas',
            'gasUsed',
            'traceId',
            'isError',
            'errCode'
        ]
    else:
        raise ValueError(f"unknown transaction type: {tr_type}")

    row_types = len(rows) * ['TEXT']
    return Table(f"{nt_type.name.lower()}_{tr_type.name.lower()}_{address}_transaction", rows, row_types)
