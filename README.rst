==============================
Welcome to ScanWatch 0.1.1dev
==============================

A local tracker of transactions for ETH address for ETH chain and BSC Chain
It is a simple interface with the `etherscan <https://etherscan.io>`_ API and the
`bscscan <https://bscscan.com>`_

Quick Tour
----------


Generate an API token on `etherscan <https://etherscan.io/myapikey>`__ or on `bscscan <https://bscscan.com/myapikey>`__.

``ScanWatch`` is not yet available on ``PYPI``, but it can be installed with ``pip``:

.. code:: bash

    pip install git+https://github.com/EtWnn/ScanWatch.git

Use your api token to initiate the manager:

.. code:: python

    from ScanWatch.Client import Client

    api_token = "<API_TOKEN>"

    client = Client(api_token)

    eth_address = "<YOUR_ETH_ADDRESS>"

    # get the ETH or BNB balance
    client.get_balance(eth_address)

    # get your ETH or BNB transactions:
    client.get_normal_transactions(eth_address)

    # get your ERC20 transactions:
    client.get_erc20_transactions(eth_address)

