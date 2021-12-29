==============================
Welcome to ScanWatch 0.1.3dev
==============================

Note
----

This library is developed and maintained by EtWnn, feel free to drop your suggestions or remarks in
the discussion tab of the git repo. You are also welcome to contribute by submitting PRs.

**Source Code:**
    https://github.com/EtWnn/ScanWatch
**Documentation:**
    https://scanwatch.readthedocs.io


This library is a local tracker of transactions for the Ethereum chain and the Binance Smart chain.
It is a simple interface with the `etherscan <https://etherscan.io>`_ and the
`bscscan <https://bscscan.com>`_ APIs and will save locally the results to gain time and avoid over-calling the APIs.

Announcement
-------

If you previously used this library with a version inferior to 0.1.3,
please head `here <https://github.com/EtWnn/ScanWatch/discussions/25>`_ to correct a potential bug in the database.


Quick Tour
----------

You will need to generate an API token to use this library.
Go on `etherscan <https://etherscan.io/myapikey>`__ for the Ethereum chain and on
`bscscan <https://bscscan.com/myapikey>`__ for the BSC chain.
(If you want to use both chains, you will need an API token for each).

``ScanWatch`` is available on `PYPI <https://pypi.org/project/ScanWatch/>`_, install with ``pip``:

.. code:: bash

    pip install ScanWatch

You can also install the latest developments (not stable):

.. code:: bash

    pip install git+https://github.com/EtWnn/ScanWatch.git@develop

You can then use your API token to instantiate the manager.

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

Once the manager is setup, you can update the locally saved transactions:

.. code:: python

    manager.update_all_transactions()
    # all transactions updated for address 0xaAC...748E8: 100%|████████████| 4/4 [00:02<00:00,  1.86it/s]

This needs to be done only when new transactions have been made since the last time you called the update method.
Otherwise you can just fetch the transactions that have been previously saved, as shown below
(see the documentation for more details).

.. code:: python

    from ScanWatch.utils.enums import TRANSACTION

    manager.get_transactions(TRANSACTION.NORMAL)  # normal transactions

    manager.get_transactions(TRANSACTION.ERC20)  # erc20 transactions

    manager.get_transactions(TRANSACTION.ERC721)  # erc721 transactions

    manager.get_transactions(TRANSACTION.INTERNAL)  # internal transactions


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

If this library has helped you in any way, feel free to donate:

- **BTC**: 14ou4fMYoMVYbWEKnhADPJUNVytWQWx9HG
- **ETH**: 0xfb0ebcf8224ce561bfb06a56c3b9a43e1a4d1be2
- **LTC**: LfHgc969RFUjnmyLn41SRDvmT146jUg9tE
- **EGLD**: erd1qk98xm2hgztvmq6s4jwtk06g6laattewp6vh20z393drzy5zzfrq0gaefh
