from brownie import config, interface, Contract, accounts
from .helpful_scripts import from_readable_amount, load_json
import time


TraderJoeQuoter = interface.LBQuoter(config['quoter']['traderjoe'])

TraderjoeRouter = interface.ILBRouter(config['router']['TraderjoeV2'])

WETH = '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
ARB = '0x912CE59144191C1204E64559FE8253a0e49E6548'

WETH_contract = interface.IWETH(WETH)


def trade():
    amount = from_readable_amount(0.000001,18)
    account = accounts.add(config["wallets"]["from_key"])
    path = [WETH, ARB]
    quote = TraderJoeQuoter.findBestPathFromAmountIn.call(path, amount)
    print(quote)

    WETH_contract.deposit({'from': account, 'value': amount})

    WETH_contract.approve(config['router']['TraderjoeV2'],amount, {'from':account})



    #TX_swap = TraderjoeRouter.exactInputSingle(ExactInputSingleParams, {'from':account})

    #TX_swap.wait(2)


def main():
    trade()