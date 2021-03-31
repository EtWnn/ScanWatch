==============================
Welcome to ETHWatch 0.1.1dev
==============================

A local tracker of transactions for ETH address
It is a simple interface with the `etherscan <https://etherscan.io>`_ API.

Quick Tour
----------


`Generate an API token <https://etherscan.io/myapikey>`_ in your etherscan account.

``ETHWatch`` is not yet available on ``PYPI``, but it can be installed with ``pip``:

.. code:: bash

    pip install git+https://github.com/EtWnn/ETHWatch.git

Use your api token to initiate the manager:

.. code:: python

    from ETHWatch.Client import Client

    api_token = "<API_TOKEN>"

    client = Client(api_token)

    eth_address = "<YOUR_ETH_ADDRESS>"

    # get the ETH balance
    client.get_balance(eth_address)

    # get your ETH transactions:
    client.get_normal_transactions(eth_address)

    # get your ERC20 transactions:
    client.get_erc20_transactions(eth_address)

