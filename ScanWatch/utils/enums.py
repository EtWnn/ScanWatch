from enum import Enum


class NETWORK(Enum):
    ETHER = 1
    BSC = 2


class TRANSACTION(Enum):
    NORMAL = 1
    INTERNAL = 2
    ERC20 = 3
    ERC721 = 4