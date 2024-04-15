from brownie import accounts, web3, interface, config, Arbitrage


min_pecentage_profit = 0.0015

# Arbitrage = interface.Arbitrage(config["Arb"]["polygon-main"]) 
# Arbi_est = web3.eth.contract( address = config["Arb"]["polygon-main"], abi = Arb.abi )

PROTOCOL_TO_ID = {
    "UniswapV2": 0, #IUniswapV2Router02
    "UniswapV3": 1,  #ISwapRouter
    "SushiswapV2": 0,
    "SushiswapV3": 1,
    "CamelotV2": 0,
    "CamelotV3": 2, #ISwapRouter_Algebra
    "RamsesV3": 1,
    "TraderjoeV2":3 #ILBRouter
}








def trade(amountIn, maxOut, maxIn, base_token, token1):
    account = accounts.add(config["wallets"]["from_key"])

    
    protocol1 = PROTOCOL_TO_ID[maxOut[1]]
    protocol2 = PROTOCOL_TO_ID[maxIn[1]]
    Router1 = config["router"][maxOut[1]]
    Router2 = config["router"][maxIn[1]]
    tokenIn_Address = web3.toChecksumAddress(base_token["address"])
    tokenOut_Address = web3.toChecksumAddress(token1["address"])
    fee1 = maxOut[2]
    fee2 = maxIn[2]
    amountOutMin1 = 0
    amountOutmin2 = 0
    
    path1 = [
        maxOut[3][0],   #binSteps[]
        maxOut[3][1],   #Versions[]
        [tokenIn_Address, tokenOut_Address] 
        ]
    path2 = [
        maxIn[3][0],   #binSteps[]
        maxIn[3][1],   #Versions[]
        [tokenOut_Address, tokenIn_Address] 
        ]

    SwapParams1 = [
        protocol1,
        Router1,
        tokenIn_Address,
        tokenOut_Address,
        fee1,
        amountIn,
        path1
    ]

    SwapParams2 = [
        protocol2,
        Router2,
        tokenOut_Address,
        tokenIn_Address,
        fee2,
        0,
        path2
    ]
    
        



    base_symbol = base_token["symbol"]
    token1_symbol = token1["symbol"]
    profit = maxIn[0] - amountIn


    try:
        Arbitrage.profitSwap([SwapParams1, SwapParams2], profit, {'from':account})
    except ValueError as e:
        print(f'Value Error: {e}')
    except Exception as e:
        print(f'Exception: {e}')

        
