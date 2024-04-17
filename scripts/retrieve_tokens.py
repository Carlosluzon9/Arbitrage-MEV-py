from brownie import config, accounts, interface, Arbitrage
from .helpful_scripts import load_json


base_tokens = load_json('base_tokens.json')
#Arbitrage = interface.Arb(config["Arb"]["polygon-main"]) 


PROTOCOLS = [
    "UniswapV2", #IUniswapV2Router02
    "UniswapV3",  #ISwapRouter
    "SushiswapV2",
    "SushiswapV3",
    "CamelotV2",
    "CamelotV3", #ISwapRouter_Algebra
    "RamsesV3",
    "TraderjoeV2" #ILBRouter
]

def retrieve():
    account = accounts.add(config["wallets"]["from_key"])
    tokens = []
    for token in base_tokens["tokens"]:
        tokens.append(token["address"])

    
    Arbitrage[0].recoverMyTokens(tokens, {"from":account})



def approve_handlers():
    tokens_list = []
    protocols_list = []
    account = accounts.add(config["wallets"]["from_key"])

    for token in base_tokens["tokens"]:
        tokens_list.append(token["address"])

    for protocol in PROTOCOLS:
        protocols_list.append(config["router"][protocol])

    Arbitrage[0].approveHandlers(tokens_list, protocols_list, {"from": account})



def send():
    account = accounts.add(config["wallets"]["from_key"])
    for token in base_tokens["tokens"]:
        IERC20 = interface.IERC20(token["address"])

        balance = IERC20.balanceOf(account.address)
        print(balance)

        if balance !=0:
            tx = IERC20.transfer(Arbitrage[0], balance, {'from': account })
            tx.wait(4)
        else:
            pass


def retrieve_one():
    account = accounts.add(config["wallets"]["from_key"])
    address = base_tokens["tokens"][5]["address"]
    tx = Arbitrage[0].recovermyTokens(address, {'from': account})



def main():
    send()