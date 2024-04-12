from brownie import config, interface, Contract, accounts
from .helpful_scripts import from_readable_amount, load_json
import time


QuickABI = load_json("interfaces/quoter.json")
RamsesQuoter = interface.IQuoterV2(config["quoter"]["ramses"])
#quickswapQuoter = Contract.from_abi('quickswapQuoter', config["quoter"]["ramses"], QuickABI)



RamsesFeeAmount ={
  'STABLE' : 50,
  'LOWEST' : 100,
  'COMPLETE' : 250,
  'LOW' : 500,
  'MEDIUM' : 3000,
  'HIGH' : 10000
}


RamsesFees = [50,100,250,500,3000,10000]
WETH = '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
address = '0x9fD5A0C972c3AE549c7C741191Ef6aE885a867f5'

RamsesSwapRouter = interface.ISwapRouter(config['router']['RamsesV3'])

WETH_contract = interface.IWETH(WETH)

ARB = '0x912CE59144191C1204E64559FE8253a0e49E6548'

    # struct ExactInputSingleParams {
    #     address tokenIn;
    #     address tokenOut;
    #     uint24 fee;
    #     address recipient;
    #     uint256 deadline;
    #     uint256 amountIn;
    #     uint256 amountOutMinimum;
    #     uint160 sqrtPriceLimitX96;
    # }



def quote():
    #account = accounts.add(config["wallets"]["from_key"])
    amount = from_readable_amount(0.000001,18)

    account = accounts.add(config["wallets"]["from_key"])


    

    # for fee in RamsesFees:
    #     ExactInputSingleParams = [WETH,ARB,amount, fee, 0]
        
    #     try:
    #         quote = quickswapQuoter.quoteExactInputSingle.call(ExactInputSingleParams)
    #         price =quote[0]
    #     except ValueError as e:
    #         price = None
    #         print(f'Value error: {e}')
    #     except Exception as e:
    #         price = None
    #         print(f'Exception: {e}')

    quoteExactInputSingleParams = [WETH,ARB,amount, 500, 0]
    try:
        quote = RamsesQuoter.quoteExactInputSingle.call(quoteExactInputSingleParams)
        tokensOut =quote[0]
    except ValueError as e:
        tokensOut = None
        print(f'Value error: {e}')

    print(f'fee:{500}, price: {tokensOut}')



    #TX_deposit = WETH_contract.deposit({'from': account, 'value': amount})

    #TX_deposit.wait(3)

        

    ExactInputSingleParams = [
        WETH,
        ARB,
        500,
        account.address,
        time.time()+100,
        amount,
        0,
        0
    ]

    WETH_contract.approve(config['router']['RamsesV3'],amount, {'from':account})

    TX_swap = RamsesSwapRouter.exactInputSingle(ExactInputSingleParams, {'from':account})

    TX_swap.wait(2)


    


    #quote = quickswapQuoter.quoteExactInputSingle.call()
    #quote = quickswapRouter.exactInputSingle.call([WMATIC, WETH, address, deadline, amount, 0, 0])




def main():
    quote()