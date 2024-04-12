from brownie import config, accounts, interface
from .helpful_scripts import load_json


base_tokens = load_json('base_tokens_polygon.json')
Arbitrage = interface.Arb(config["Arb"]["polygon-main"]) 


def retrieve():
    account = accounts.add(config["wallets"]["from_key"])
    tokens = []
    for token in base_tokens["tokens"]:
        tokens.append(token["address"])

    
    Arbitrage.recoverMyTokens(tokens, {"from":account})



def send():
    account = accounts.add(config["wallets"]["from_key"])
    for token in base_tokens["tokens"]:
        IERC20 = interface.IERC20(token["address"])

        balance = IERC20.balanceOf(account.address)
        print(balance)


        tx = IERC20.transfer(config["Arb"]["polygon-main"], balance, {'from': account, 'priority_fee':36000000000})
        tx.wait(4)



def retrieve_one():
    account = accounts.add(config["wallets"]["from_key"])
    address = base_tokens["tokens"][5]["address"]
    tx = Arbitrage.recoverTokens(address, {'from': account})



def main():
    send()