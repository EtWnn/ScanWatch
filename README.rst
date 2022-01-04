==============================
Welcome to ScanWatch 0.2.0dev
==============================


Note
----

This library is developed and maintained by EtWnn, feel free to drop your suggestions or remarks in
the discussion tab of the git repo. You are also welcome to contribute by submitting PRs.

**Source Code:**
    https://github.com/EtWnn/ScanWatch
**Documentation:**
    https://scanwatch.readthedocs.io


This library is a local tracker of transactions for the Ethereum chain, the Binance Smart chain and the Polygon chain.
It is a simple single-point interface with the `etherscan <https://etherscan.io>`_, `bscscan <https://bscscan.com>`_ and
`polygonscan <https://polygonscan.com>`_ APIs.
This library will save locally the transactions to gain time and avoid over-calling the APIs.


Announcement
------------

|siren||siren||siren|

If you previously used this library with a version inferior to 0.1.3,
please head `here <https://github.com/EtWnn/ScanWatch/discussions/25>`_ to correct a potential bug in the database.

|siren||siren||siren|


Quick Tour
----------

1. API Keys
~~~~~~~~~~~~

You will need to generate an API token to use this library:

1. Ethereum chain: go on `etherscan <https://etherscan.io/myapikey>`_
2. Binance Smart chain: go on `bscscan <https://bscscan.com/myapikey>`_
3. Polygon chain: go on `polygonscan <https://polygonscan.com/myapikey>`_

(If you want to use several chains, you will need an API token for each).

2. Installation
~~~~~~~~~~~~~~~~

``ScanWatch`` is available on `PYPI <https://pypi.org/project/ScanWatch/>`_, install with ``pip``:

.. code:: bash

    pip install ScanWatch

You can also install the latest developments (not stable):

.. code:: bash

    pip install git+https://github.com/EtWnn/ScanWatch.git@develop

3. Manager
~~~~~~~~~~

The manager is the object that you will use to update and get the transactions.

The manager is instantiated with an API token and an address.

Example for Ethereum:

.. code:: python

    from ScanWatch.ScanManager import ScanManager
    from ScanWatch.utils.enums import NETWORK

    api_token = "<ETH_API_TOKEN>"
    address = "<YOUR_ETH_ADDRESS>"

    manager = ScanManager(address, NETWORK.ETHER, api_token)

Example for BSC:

.. code:: python

    from ScanWatch.ScanManager import ScanManager
    from ScanWatch.utils.enums import NETWORK

    api_token = "<BSC_API_TOKEN>"
    address = "<YOUR_BSC_ADDRESS>"

    manager = ScanManager(address, NETWORK.BSC, api_token)

4. Transactions Update
~~~~~~~~~~~~~~~~~~~~~~

Once the manager is setup, you can update the locally saved transactions:

.. code:: python

    manager.update_all_transactions()
    # all transactions updated for address 0xaAC...748E8: 100%|████████████| 4/4 [00:02<00:00,  1.86it/s]

This needs to be done only when new transactions have been made since the last time you called the update method.

5. Transactions
~~~~~~~~~~~~~~~

To fetch the transactions that have been previously saved, just use the methods below.
(see the `documentation <https://scanwatch.readthedocs.io>`_ for more details).

.. code:: python

    from ScanWatch.utils.enums import TRANSACTION

    manager.get_transactions(TRANSACTION.NORMAL)  # normal transactions

    manager.get_transactions(TRANSACTION.ERC20)  # erc20 transactions

    manager.get_transactions(TRANSACTION.ERC721)  # erc721 transactions

    manager.get_transactions(TRANSACTION.INTERNAL)  # internal transactions

6. Holdings
~~~~~~~~~~~~

The manager can also give you the current tokens hold by an address:

For erc20 tokens:

.. code:: python

    manager.get_erc20_holdings()


.. code:: bash

    {
        'USDC': Decimal('50'),
        'AllianceBlock Token': Decimal('12458.494516884'),
        'Blockchain Certified Data Token': Decimal('75174'),
        'Compound': Decimal('784.24998156'),
        'ZRX': Decimal('3.1')
    }

For erc721 tokens:

.. code:: python

    manager.get_erc721_holdings()


.. code:: bash

    [
        {
            'contractAddress': '0x8azd48c9ze46azx1e984fraz4da9zz8dssad49ct',
            'tokenID': '78941',
            'count': 1,
            'tokenName': 'SUPER NFT GAME',
            'tokenSymbol': 'Hero'
        },
        {
            'contractAddress': '0x6edd39bdba2fazs3db5fxd86908789cbd905f04d',
            'tokenID': '33001',
            'count': 1,
            'tokenName': 'MY FAV NFT ARTIST HANDMADE THIS',
            'tokenSymbol': 'dubious thing'
        }
    ]


Main / test nets
----------------

If you want to switch from main to test nets, you can specify the net name at the manager creation:

.. code:: python

    manager = ScanManager(address, <network>, api_token, <net_name>)

Supported nets are:
    - For Ethereum: "main", "goerli", "kovan", "rinkeby", "ropsten"
    - For BSC: "main", "test"


Donation
--------

If this library has helped you in any way, feel free to help me |blush|

With your donation, I will be able to keep working on this project and add new features. Thank you!

- **BTC**: 14ou4fMYoMVYbWEKnhADPJUNVytWQWx9HG
- **ETH**: 0xfb0ebcf8224ce561bfb06a56c3b9a43e1a4d1be2
- **LTC**: LfHgc969RFUjnmyLn41SRDvmT146jUg9tE
- **EGLD**: erd1qk98xm2hgztvmq6s4jwtk06g6laattewp6vh20z393drzy5zzfrq0gaefh

.. |siren| replace:: 🚨
.. |blush| replace:: 😊