from brownie import config, accounts, Arbitrage, web3




def deploy():
    account = accounts.add(config["wallets"]["from_key"])
    #print(Arb.abi)
    #mock = web3.eth.contract(address=config["Arb"]["polygon-main"] , abi=Arb.abi)

    #estimated_gas = mock.functions.recoverTokens('0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6').estimateGas({'from':account.address})
    Arbitrage.deploy({'from':account})
    #print(estimated_gas)

def main():
    deploy()